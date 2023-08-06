"""
SimplerNetV1 in Pytorch.

The implementation is based on :
https://github.com/D-X-Y/ResNeXt-DenseNet

Added Bregman version - J.Frecon
"""
import torch
import torch.nn as nn
from torch.autograd import Variable
import torch.nn.functional as F
import bregmanet.networks.utils.activation as act


class LambdaLayer(nn.Module):
    def __init__(self, lambd):
        super(LambdaLayer, self).__init__()
        self.lambd = lambd

    def forward(self, x):
        return self.lambd(x)


class simplenet(nn.Module):
    def __init__(self, classes=10):
        super(simplenet, self).__init__()
        self.features = self._make_layers()
        self.classifier = nn.Linear(256, classes)
        self.drp = nn.Dropout(0.1)

    def forward(self, x):
        out = self.features(x)

        #Global Max Pooling
        out = F.max_pool2d(out, kernel_size=out.size()[2:]) 
        # out = F.dropout2d(out, 0.1, training=True)
        out = self.drp(out)

        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out

    def _make_layers(self):

        model = nn.Sequential(
                             nn.Conv2d(3, 64, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(64, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(64, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 128, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(128, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                             nn.Conv2d(128, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),



                             nn.Conv2d(256, 512, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(512, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(512, 2048, kernel_size=[1, 1], stride=(1, 1), padding=(0, 0)),
                             nn.BatchNorm2d(2048, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),



                             nn.Conv2d(2048, 256, kernel_size=[1, 1], stride=(1, 1), padding=(0, 0)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),


                             nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
                             nn.Dropout2d(p=0.1),


                             nn.Conv2d(256, 256, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(256, eps=1e-05, momentum=0.05, affine=True),
                             nn.ReLU(inplace=True),

                            )

        for m in model.modules():
          if isinstance(m, nn.Conv2d):
            nn.init.xavier_uniform_(m.weight.data, gain=nn.init.calculate_gain('relu'))

        return model


class bregman_simplenet(nn.Module):
    def __init__(self, classes=10, activation='atan'):
        super(bregman_simplenet, self).__init__()
        self.features = self._make_layers()
        self.classifier = nn.Linear(256, classes)
        self.drp = nn.Dropout(0.1)
        self.activation, self.inverse, self.range = act.get(activation, version='bregman')

    def forward(self, x):
        out = self.features(x)
        out = F.max_pool2d(out, kernel_size=out.size()[2:])
        out = self.drp(out)
        out = out.view(out.size(0), -1)
        out = self.classifier(out)
        return out

    def _make_shortcut(self, planes, option='C'):

        self.shortcut = nn.Sequential()
        if option == 'A':
            self.shortcut = nn.Sequential(
                LambdaLayer(lambda x:
                            F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, planes // 4, planes // 4), "constant", 0)),
                LambdaLayer(lambda x: self.activation(x)),
                LambdaLayer(lambda x: self.inverse(x))
            )
        elif option == 'B':
            self.shortcut = nn.Sequential(
                LambdaLayer(lambda x:
                            F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, planes // 4, planes // 4), "constant", 0))
            )
        elif option == 'C':
            " The padding value is such that, after the inverse activation, it is 0 "
            val = float(self.activation(torch.zeros(1)))
            self.shortcut = LambdaLayer(lambda x: F.pad(x[:, :, ::2, ::2], (0, 0, 0, 0, planes // 4, planes // 4),
                                                        "constant", val))
        return self.shortcut

    def _make_bock(self, x, in_planes, out_planes):

        #shortcut = self._make_shortcut(planes=out_planes)
        if in_planes == out_planes:
            shortcut = x
        else:
            shortcut = 0
        model = nn.Sequential(
                             nn.Conv2d(in_planes, out_planes, kernel_size=[3, 3], stride=(1, 1), padding=(1, 1)),
                             nn.BatchNorm2d(out_planes, eps=1e-05, momentum=0.05, affine=True),
        )
        x = self.activation(shortcut + model(x))

        return x

    def _make_layers(self):

        model = nn.Sequential(
            LambdaLayer(lambda x: self._make_bock(x, 3, 64)),
            LambdaLayer(lambda x: self._make_bock(x, 64, 128)),
            LambdaLayer(lambda x: self._make_bock(x, 128, 128)),
            LambdaLayer(lambda x: self._make_bock(x, 128, 128)),

            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
            nn.Dropout2d(p=0.1),

            LambdaLayer(lambda x: self._make_bock(x, 128, 128)),
            LambdaLayer(lambda x: self._make_bock(x, 128, 128)),
            LambdaLayer(lambda x: self._make_bock(x, 128, 256)),

            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
            nn.Dropout2d(p=0.1),

            LambdaLayer(lambda x: self._make_bock(x, 256, 256)),
            LambdaLayer(lambda x: self._make_bock(x, 256, 256)),

            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
            nn.Dropout2d(p=0.1),

            LambdaLayer(lambda x: self._make_bock(x, 256, 512)),

            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
            nn.Dropout2d(p=0.1),

            LambdaLayer(lambda x: self._make_bock(x, 512, 2048)),
            LambdaLayer(lambda x: self._make_bock(x, 2048, 256)),

            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 2), dilation=(1, 1), ceil_mode=False),
            nn.Dropout2d(p=0.1),

            LambdaLayer(lambda x: self._make_bock(x, 256, 256)),
        )

        # for m in model.modules():
       #      if isinstance(m, nn.Conv2d):
        #         nn.init.xavier_uniform_(m.weight.data, gain=nn.init.calculate_gain('relu'))

        return model
