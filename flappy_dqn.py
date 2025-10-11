# flappy_dqn_colab_interactive_fixed.py
import gymnasium as gym
import flappy_bird_gymnasium
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
import plotly.graph_objects as go
from IPython.display import display
import imageio
from google.colab import output
import numpy as np

output.enable_custom_widget_manager()

env = gym.make("FlappyBird-v0", render_mode="rgb_array")

class RewardShapingWrapper(gym.Wrapper):
    def step(self, action):
        obs, reward, done, trunc, info = self.env.step(action)
        bird_velocity = obs[1]
        pipe_y = obs[3]
        reward = 1.0
        reward -= 0.01 * abs(bird_velocity)
        if action == 1:
            reward -= 0.05
        reward -= 0.02 * abs(obs[0] - pipe_y)
        if "pipe_passed" in info and info["pipe_passed"]:
            reward += 5.0
        return obs, reward, done, trunc, info

env = RewardShapingWrapper(env)

class LivePlotlyCallback(BaseCallback):
    def __init__(self, verbose=0, plot_every=100):
        super().__init__(verbose)
        self.plot_every = plot_every
        self.rewards = []
        self.lengths = []
        self.velocities = []
        self.actions = []

        # interactive figure
        self.fig = go.FigureWidget()
        self.fig.add_scatter(name="Reward")
        self.fig.add_scatter(name="Episode Length")
        self.fig.add_scatter(name="Velocity")
        self.fig.add_scatter(name="Action")
        display(self.fig)

    def _on_step(self) -> bool:
        if self.n_calls % self.plot_every == 0:
            if "infos" in self.locals:
                for info in self.locals["infos"]:
                    if "episode" in info:
                        ep_info = info["episode"]
                        self.rewards.append(ep_info["r"])
                        self.lengths.append(ep_info["l"])
                        # Use latest obs and action if available
                        self.velocities.append(self.locals.get("obs", np.array([0, 0]))[1])
                        self.actions.append(self.locals.get("action", 0))

            with self.fig.batch_update():
                self.fig.data[0].y = self.rewards
                self.fig.data[1].y = self.lengths
                self.fig.data[2].y = self.velocities
                self.fig.data[3].y = self.actions
        return True

callback = LivePlotlyCallback(plot_every=100)

model = DQN(
    "MlpPolicy",
    env,
    learning_rate=5e-5,
    buffer_size=100_000,
    learning_starts=10_000,
    batch_size=32,
    gamma=0.995,
    train_freq=4,
    target_update_interval=1_000,
    verbose=1,
    tensorboard_log="./flappy_tensorboard_colab/",
    exploration_fraction=0.1,
    exploration_final_eps=0.01
)

model.learn(total_timesteps=1000_000, callback=callback)
model.save("flappy_dqn")

obs, info = env.reset()
done = False
frames = []

while not done:
    action, _ = model.predict(obs)
    obs, reward, done, trunc, info = env.step(action)
    frame = env.render()
    if frame is not None:
        frames.append(frame)
    done = done or trunc

imageio.mimsave("flappy_dqn.gif", frames, duration=1000/30)
print("Saved GIF as flappy_dqn.gif")

from IPython.display import Image
Image("flappy_dqn.gif")
