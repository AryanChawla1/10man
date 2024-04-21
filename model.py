import os
import pandas as pd
import torch.nn as nn
from torch import from_numpy, float32, optim, save, clamp
from torch.utils.data import DataLoader, TensorDataset
from torchvision import datasets, transforms

# Define Model


class Scorer(nn.Module):
    def __init__(self):
        super().__init__()
        # create stack
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(29, 256),
            nn.ReLU(),
            nn.Linear(256, 256),
            nn.ReLU(),
            nn.Linear(256, 1),
        )

    # forward pass
    def forward(self, x):
        output = self.linear_relu_stack(x)
        output = clamp(output, min=0, max=10)
        return output


df = pd.read_csv('data.csv', sep=",")
x = from_numpy(df.iloc[:, :-1].values).to(float32)
y = from_numpy(df.iloc[:, -1].values).to(float32)
dataset = TensorDataset(x, y)

batch_size = 64
dataloader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

model = Scorer()

criterion = nn.MSELoss()
optimizier = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 200
target_loss = 0.3
for epoch in range(num_epochs):
    model.train()
    total_loss = 0
    for batch_x, batch_y in dataloader:
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y.unsqueeze(1))

        optimizier.zero_grad()
        loss.backward()
        optimizier.step()

        total_loss += loss.item() * batch_x.size(0)

    average_loss = total_loss / len(dataset)
    print(f"Epoch [{epoch + 1}/{num_epochs}], Loss: {average_loss:.4f}")

    if average_loss < target_loss:
        print("Target loss reached. Training stopped")
        break

save(model.state_dict(), 'trained_model.pth')
