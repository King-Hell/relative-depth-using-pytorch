import torch
from torch import nn
from layers.inception import inception

class Channels1(nn.Module):
	def __init__(self):
		super(Channels1, self).__init__()
		self.list = nn.ModuleList()
		self.list.add_module('EE',
			nn.Sequential(
				inception(256,[[64],[3,32,64],[5,32,64],[7,32,64]]),
				inception(256,[[64],[3,32,64],[5,32,64],[7,32,64]])
				)
			)
		self.list.add_module('EEE',
			nn.Sequential(
				nn.AvgPool2d(2),
				inception(256,[[64],[3,32,64],[5,32,64],[7,32,64]]),
				inception(256,[[64],[3,32,64],[5,32,64],[7,32,64]]),
				inception(256,[[64],[3,32,64],[5,32,64],[7,32,64]]), 
				nn.UpsamplingNearest2d(scale_factor=2)
				)
			)

	def forward(self,x):
		return self.list[0](x)+self.list[1](x)

class Channels2(nn.Module):
	def __init__(self):
		super(Channels2, self).__init__()
		self.list = nn.ModuleList()
		self.list.add_module('EF',
			nn.Sequential(
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				inception(256, [[64], [3,64,64], [7,64,64], [11,64,64]])
				)
			)
		self.list.add_module('EE1EF', 
			nn.Sequential(
				nn.AvgPool2d(2),
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				Channels1(),
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				inception(256, [[64], [3,64,64], [7,64,64], [11,64,64]]),
				nn.UpsamplingNearest2d(scale_factor=2)
				)
			)

	def forward(self,x):
		return self.list[0](x)+self.list[1](x)

class Channels3(nn.Module):
	def __init__(self):
		super(Channels3, self).__init__()
		self.list = nn.ModuleList()
		self.list.add_module(
			'BD2EG',
			nn.Sequential(
				nn.AvgPool2d(2),
				inception(128, [[32], [3,32,32], [5,32,32], [7,32,32]]),
				inception(128, [[64], [3,32,64], [5,32,64], [7,32,64]]),
				Channels2(),
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				inception(256, [[32], [3,32,32], [5,32,32], [7,32,32]]), 
				nn.UpsamplingNearest2d(scale_factor=2)
				)
			)
		self.list.add_module(
			'EF',
			nn.Sequential(
				inception(256, [[64], [3,32,64], [5,32,64], [7,32,64]]), 
				inception(256, [[64], [3,64,64], [7,64,64], [11,64,64]])
				)
			)

	def forward(self,x):
		return self.list[0](x)+self.list[1](x)

class Channels4(nn.Module):
	def __init__(self):
		super(Channels4, self).__init__()
		self.list = nn.ModuleList()
		self.list.add_module(
			'BB3BA',
			nn.Sequential(
				nn.AvgPool2d(2),
				inception(128, [[32], [3,32,32], [5,32,32], [7,32,32]]),
				inception(128, [[32], [3,32,32], [5,32,32], [7,32,32]]),
				Channels3(),
				inception(128, [[32], [3,64,32], [5,64,32], [7,64,32]]),
				inception(128, [[16], [3,32,16], [7,32,16], [11,32,16]]),
				nn.UpsamplingNearest2d(scale_factor=2)
				)
			)
		self.list.add_module(
			'A',
			nn.Sequential(
				inception(128, [[16], [3,32,16], [7,32,16], [11,32,16]])
				)
			)

	def forward(self,x):
		return self.list[0](x)+self.list[1](x)


class Model(nn.Module):
	def __init__(self):
		super(Model, self).__init__()

		# first layer
		self.blockH = nn.Sequential()
		self.blockH.add_module('conv', nn.Conv2d(3,128,7,padding=3))
		self.blockH.add_module('norm', nn.BatchNorm2d(128))
		self.blockH.add_module('relu', nn.ReLU(True))

		self._4channels = Channels4()

		self.final = nn.Conv2d(64,1,3,padding=1)

	def forward(self,x):
		return final(_4channels(blockH(x)))

		
if __name__ == '__main__':
	test = Model()
	print(test)
