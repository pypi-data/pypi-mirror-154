import torch.nn as nn
import bregmanet.networks.utils.activation as activation
import bregmanet.networks.utils.weight as weight
import torch


class MLP(nn.Module):
    """
    Multilayer Perceptron
    """

    def __init__(self, activation_name, version='standard', num_neurons=None, input_dim=None, output_dim=1,
                 init='random', weight_norm=False, num_iterations=1):
        super().__init__()
        version = version.lower()
        activation_name = activation_name.lower()
        init_param = weight.parameter_initialization(version=version, init_type=init)

        # Parameters
        self.num_neurons = [input_dim] if num_neurons is None else num_neurons
        self.num_layers = self.num_neurons.__len__()
        self.weight_norm = weight_norm
        self.num_iterations = num_iterations
        self.version = version

        # Hidden layers
        self.lin = nn.ModuleList()
        self.reparametrization = nn.ModuleList()
        for in_neurons, out_neurons in zip([input_dim] + self.num_neurons[:self.num_layers - 1], self.num_neurons):

            # Linear part associated to the offset
            if in_neurons == out_neurons or self.version == 'standard':
                # ... then no need to initialize
                self.reparametrization.append(nn.Identity())
            else:
                # ... then initialize with random weights on the simplex
                self.reparametrization.append(weight.linear_with_init(in_neurons, out_neurons, init='simplex'))

            # Classical linear part
            self.lin.append(weight.linear_with_init(in_neurons, out_neurons, init=init_param['hidden'],
                                                    weight_norm=weight_norm))
        self.activation, self.offset, self.range = activation.get(activation_name=activation_name, version=version)

        # Output layer
        self.output = weight.linear_with_init(self.num_neurons[-1], output_dim, init=init_param['output']) \
        #    if self.num_neurons[-1] > 1 \
        #    else nn.Identity()

    def forward(self, xb):

        # Hidden layers
        for idl in range(self.num_layers):

            # Constraint on offset weights
            if self.version == 'bregman':
                self.reparametrization[idl] = weight.constraint(self.reparametrization[idl])

            # Perform forward pass
            for _ in range(self.num_iterations):
                if self.version == 'bregman':
                    xoffset = torch.clamp(self.reparametrization[idl](xb), self.range[0], self.range[1])
                    xb = self.activation(self.offset(xoffset) + self.lin[idl](xb))
                else:
                    xb = self.activation(self.lin[idl](xb))

        # Output layer
        xb = self.output(xb)

        return xb
