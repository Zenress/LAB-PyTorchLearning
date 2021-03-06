import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

  def __init__(self):
    super(Net, self).__init__()
    #1 Input image channel, 6 output channels, 5x5 square convolution kernel
    self.conv1 = nn.Conv2d(1,6,5)
    self.conv2 = nn.Conv2d(6,16,5)
    #An affine operation: y = Wx + b
    self.fc1 = nn.Linear(16 * 5 * 5, 120) #5x5 from image dimension
    self.fc2 = nn.Linear(120,84)
    self.fc3 = nn.Linear(84,10)

  def forward(self, x):
    #Max pooling over a (2, 2) window
    x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
    #If the size is a square, you can specify with a single number
    x = F.max_pool2d(F.relu(self.conv2(x)), 2)
    x = torch.flatten(x, 1) #Flatten all dimensions except the batch dimension
    x = F.relu(self.fc1(x))
    x = F.relu(self.fc2(x))
    x = self.fc3(x)
    return x

net = Net()
print(net)

params = list(net.parameters())
print(len(params))
print(params[0].size()) #Conv1's .weight

input = torch.randn(1,1,32,32)
out = net(input)
print(out)

net.zero_grad()
out.backward(torch.randn(1,10))

output = net(input)
target = torch.randn(10) #A dummy target for example
target = target.view(1,-1) #Make it the same shape as output
criterion = nn.MSELoss()

loss = criterion(output, target)
print(loss)

print(loss.grad_fn) #MSE Loss
print(loss.grad_fn.next_functions[0][0]) #Linear layer
print(loss.grad_fn.next_functions[0][0].next_functions[0][0]) #ReLU

net.zero_grad() #Zeroes the gradient buffers of all parameters

print("conv.bias.grad before backward")
print(net.conv1.bias.grad)

loss.backward()

print("conv1.bias.grad after backward")
print(net.conv1.bias.grad)

learning_rate = 0.1
for f in net.parameters():
  f.data.sub_(f.grad.data * learning_rate)

import torch.optim as optim

#Create your optimizer
optimizer = optim.SGD(net.parameters(), lr=0.01)

#In your training loop:
optimizer.zero_grad() #Zero the gradient buffers
output = net(input)
loss = criterion(output, target)
loss.backward()
optimizer.step() #Does the update