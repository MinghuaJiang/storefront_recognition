require 'image'
require 'nn'

torch.setdefaulttensortype('torch.FloatTensor')

trainset = torch.load('../model/cifar10-train.t7') -- training images.
valset = torch.load('../model/cifar10-val.t7')  -- validation set used to evaluate the model and tune parameters.
trainset.label = trainset.label + 1
valset.label = valset.label + 1
classes = {'airplane', 'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck'}

-- Let's show all images of frogs.
id2classes = {}  -- Build a mapping between object names and class ids.
-- Remember that tables in lua are similar to (key,value) collections e.g. hashmaps.
for k,v in pairs(classes) do id2classes[k] = v end

trainset.normdata = trainset.data:clone():float()
valset.normdata = valset.data:clone():float()
cifarMean = {trainset.normdata[{{}, {1}, {}, {}}]:mean(),
             trainset.normdata[{{}, {2}, {}, {}}]:mean(),
             trainset.normdata[{{}, {3}, {}, {}}]:mean()}

cifarStd = {trainset.normdata[{{}, {1}, {}, {}}]:std(),
            trainset.normdata[{{}, {2}, {}, {}}]:std(),
            trainset.normdata[{{}, {3}, {}, {}}]:std()}

meanstd = {}
meanstd.mean = cifarMean
meanstd.std = cifarStd

for i  = 1, 3 do
    -- Subtracting the mean on each channel makes the values roughly between -128 and 128.
    trainset.normdata[{{}, {i}, {}, {}}]:add(-cifarMean[i])
    valset.normdata[{{}, {i}, {}, {}}]:add(-cifarMean[i])
    -- Dividing the std on each channel makes the values roughly between -1 and 1.
    trainset.normdata[{{}, {i}, {}, {}}]:div(cifarStd[i])
    valset.normdata[{{}, {i}, {}, {}}]:div(cifarStd[i])
end


local criterion = nn.ClassNLLCriterion() -- Negative log-likelihood criterion.
-- params is a flat vector with the concatenation of all the parameters inside model.
-- gradParams is a flat vector with the concatenation of all the gradients of parameters inside the model.
-- These two variables also merely point to the internal individual parameters in each layer of the module.

function trainModel(model, opt, features, preprocessFn)
    -- Get all the parameters (and gradients) of the model in a single vector.
    local params, gradParams = model:getParameters()

    local opt = opt or {}
    local batchSize = opt.batchSize or 64  -- The bigger the batch size the most accurate the gradients.
    local learningRate = opt.learningRate or 0.001  -- This is the learning rate parameter often referred to as lambda.
    local momentumRate = opt.momentumRate or 0.9
    local numEpochs = opt.numEpochs or 3
    local velocityParams = torch.zeros(gradParams:size())
    local train_features, val_features
    if preprocessFn then
        train_features = trainset.data:float():div(255)
        val_features = valset.data:float():div(255)
    else
        train_features = (features and features.train_features) or trainset.normdata
        val_features = (features and features.val_features) or valset.normdata
    end
    -- Go over the training data this number of times.
    for epoch = 1, numEpochs do
        local sum_loss = 0
        local correct = 0
        
        -- Run over the training set samples.
        model:training()
        for i = 1, trainset.normdata:size(1) / batchSize do
            
            -- 1. Sample a batch.
            local inputs
            if preprocessFn then
                inputs = torch.Tensor(batchSize, 3, 224, 224)
            else
                inputs = (features and torch.Tensor(batchSize, 4096)) or torch.Tensor(batchSize, 3, 32, 32)
            end
            local labels = torch.Tensor(batchSize)
            for bi = 1, batchSize do
                local rand_id = torch.random(1, train_features:size(1))
                if preprocessFn then
                    inputs[bi] = preprocessFn(train_features[rand_id])
                else
                    inputs[bi] = train_features[rand_id]
                end
                labels[bi] = trainset.label[rand_id]
            end
            -- 2. Perform the forward pass (prediction mode).
            local predictions = model:forward(inputs)
            
            -- 3. Evaluate results.
            for i = 1, predictions:size(1) do
                local _, predicted_label = predictions[i]:max(1)
                if predicted_label[1] == labels[i] then correct = correct + 1 end
            end
            sum_loss = sum_loss + criterion:forward(predictions, labels)

            -- 4. Perform the backward pass (compute derivatives).
            -- This zeroes-out all the parameters inside the model pointed by variable params.
            model:zeroGradParameters()
            -- This internally computes the gradients with respect to the parameters pointed by gradParams.
            local gradPredictions = criterion:backward(predictions, labels)
            model:backward(inputs, gradPredictions)

            -- 5. Perform the SGD update.
            velocityParams:mul(momentumRate)
            velocityParams:add(learningRate, gradParams)
            params:add(-1, velocityParams)

            if i % 100 == 0 then  -- Print this every five thousand iterations.
                print(('train epoch=%d, iteration=%d, avg-loss=%.6f, avg-accuracy = %.2f')
                    :format(epoch, i, sum_loss / i, correct / (i * batchSize)))
            end
        end

        -- Run over the validation set for evaluation.
        local validation_accuracy = 0
        local nBatches = val_features:size(1) / batchSize
        model:evaluate()
        for i = 1, nBatches do
            
            -- 1. Sample a batch.
            if preprocessFn then
                inputs = torch.Tensor(batchSize, 3, 224, 224)
            else
                inputs = (features and torch.Tensor(batchSize, 4096)) or torch.Tensor(batchSize, 3, 32, 32)
            end
            local labels = torch.Tensor(batchSize)
            for bi = 1, batchSize do
                local rand_id = torch.random(1, val_features:size(1))
                if preprocessFn then
                    inputs[bi] = preprocessFn(val_features[rand_id])
                else
                    inputs[bi] = val_features[rand_id]
                end
                labels[bi] = valset.label[rand_id]
            end

            -- 2. Perform the forward pass (prediction mode).
            local predictions = model:forward(inputs)
            
            -- 3. evaluate results.
            for i = 1, predictions:size(1) do
                local _, predicted_label = predictions[i]:max(1)
                if predicted_label[1] == labels[i] then validation_accuracy = validation_accuracy + 1 end
            end
        end
        validation_accuracy = validation_accuracy / (nBatches * batchSize)
        print(('\nvalidation accuracy at epoch = %d is %.4f'):format(epoch, validation_accuracy))
    end
end


local model = nn.Sequential()
model:add(nn.SpatialConvolution(3, 8, 5, 5))  -- 3 input channels, 8 output channels (8 filters), 5x5 kernels.
model:add(nn.SpatialBatchNormalization(8, 1e-3))  -- BATCH NORMALIZATION LAYER.
model:add(nn.ReLU())
model:add(nn.SpatialMaxPooling(2, 2, 2, 2)) -- Max pooling in 2 x 2 area.
model:add(nn.SpatialConvolution(8, 16, 5, 5))  -- 8 input channels, 16 output channels (16 filters), 5x5 kernels.
model:add(nn.SpatialBatchNormalization(16, 1e-3))  -- BATCH NORMALIZATION LAYER.
model:add(nn.ReLU())                      
model:add(nn.SpatialMaxPooling(2, 2, 2, 2))  -- Max pooling in 2 x 2 area.
model:add(nn.View(16*5*5))    -- Vectorize the output of the convolutional layers.
model:add(nn.Linear(16*5*5, 120))
model:add(nn.ReLU())
model:add(nn.Linear(120, 84))
model:add(nn.ReLU())  
model:add(nn.Linear(84, 10))
model:add(nn.LogSoftMax())

opt = {}
opt.learningRate = 0.02 -- bigger learning rate worked best for this network.
opt.batchSize = 32  -- smaller batch size, less accurate gradients, but more frequent updates.
opt.numEpochs = 5
trainModel(model, opt) 

torch.save('../model/test_model.t7', model)
torch.save('../model/test_classes.t7',id2classes)
torch.save('../model/test_meanstd.t7',meanstd)
