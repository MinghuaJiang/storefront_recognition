require 'nn'

function createModel()
   local features = nn.Sequential()
   features:add(nn.SpatialConvolution(3,64,11,11,4,4,2,2))       -- 224 -> 55
   features:add(nn.SpatialBatchNormalization(64,1e-3))
   features:add(nn.ReLU(true))
   features:add(nn.SpatialMaxPooling(3,3,2,2))                   -- 55 ->  27
   features:add(nn.SpatialConvolution(64,192,5,5,1,1,2,2))       --  27 -> 27
   features:add(nn.SpatialBatchNormalization(192,1e-3))
   features:add(nn.ReLU(true))
   features:add(nn.SpatialMaxPooling(3,3,2,2))                   --  27 ->  13
   features:add(nn.SpatialConvolution(192,384,3,3,1,1,1,1))      --  13 ->  13
   features:add(nn.SpatialBatchNormalization(384,1e-3))
   features:add(nn.ReLU(true))
   features:add(nn.SpatialConvolution(384,256,3,3,1,1,1,1))      --  13 ->  13
   features:add(nn.SpatialBatchNormalization(256,1e-3))
   features:add(nn.ReLU(true))
   features:add(nn.SpatialConvolution(256,256,3,3,1,1,1,1))      --  13 ->  13
   features:add(nn.SpatialBatchNormalization(256,1e-3))
   features:add(nn.ReLU(true))
   features:add(nn.SpatialMaxPooling(3,3,2,2))                   -- 13 -> 6


   -- 1.3. Create Classifier (fully connected layers)
   local classifier = nn.Sequential()
   classifier:add(nn.View(256*6*6))
   classifier:add(nn.Dropout(0.5))
   classifier:add(nn.Linear(256*6*6, 4096))
   classifier:add(nn.BatchNormalization(4096,1e-3))
   classifier:add(nn.ReLU(true))
   classifier:add(nn.Dropout(0.5))
   classifier:add(nn.Linear(4096, 4096))
   classifier:add(nn.BatchNormalization(4096,1e-3))
   classifier:add(nn.ReLU(true))
   classifier:add(nn.Linear(4096, 1000))
   classifier:add(nn.LogSoftMax())

   -- 1.4. Combine 1.1 and 1.3 to produce final model
   local model = nn.Sequential():add(features):add(classifier)
   model.imageSize = 256
   model.imageCrop = 224
   print(model)
   return model
end

