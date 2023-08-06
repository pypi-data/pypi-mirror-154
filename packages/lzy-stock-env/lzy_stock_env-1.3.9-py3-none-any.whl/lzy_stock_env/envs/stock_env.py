import gym
from gym import spaces
import numpy as np
from gym.utils import seeding
import torch
from typing import Optional

class LzyEnv(gym.Env):
    # metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, pred_df ,normal_prices, real_price):
        # assert render_mode is None or render_mode in self.metadata["render_modes"]
        self._real_price = real_price
        self._pred = pred_df
        self._normal_prices = normal_prices
        self.observation_space = spaces.Dict(
            {  # state的含义分别是：持仓比例，6个LSTM的预测结果，还有1个当前价值。
                "state": spaces.Box(0, 1, shape=(8,), dtype=np.float32),
                # day用于判断是否结束一轮
                "day": spaces.Box(0, 10000, shape=(1,), dtype=int),
                # price分别是股票开盘，最高，最低，收盘价格
                "price": spaces.Box(0, 100, shape=(4,), dtype=np.float32),
                #asset指智能体的资产量
                "asset": spaces.Box(0,100000000,shape=(1,0),dtype=np.float32)
            }
        )
        #5种持仓状态：0%，25%，50%，75%，100%。
        self.action_space = spaces.Discrete(5)
        self._action_to_position = {
            0: torch.tensor([0.0]),
            1: torch.tensor([0.25]),
            2: torch.tensor([0.50]),
            3: torch.tensor([0.75]),
            4: torch.tensor([1.0]),
        }

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def _get_obs(self):
        return {"pos":torch.tensor(self._position),
                "pred":torch.tensor(self._pred.iloc[self._day]),
                "price":torch.tensor(self._real_price.iloc[self._day]),
                "normal":torch.tensor(self._normal_prices.iloc[self._day])}

    def _get_info(self):
        return {"asset": self._asset}

    def _get_reward(self):
        return

    def _get_normal(self):
        return np.ndarray([self._normal_prices.iloc[self._day]])

    def _get_price(self):
        return np.ndarray([self._real_price[self._day]])

    def reset(self, return_info=False, options=None):
        self._asset = 100
        self._day = 0
        self._position = torch.tensor([0])
        self._normal = self._get_normal()
        self._price = self._get_price()
        observation = self._get_obs()
        info = self._get_info()
        return (observation, info) if return_info else observation

    def step(self, action):
        past_asset = self._asset
        past_price = self._get_price()
        self._position = self._action_to_position[action]
        self._day += 1
        self._asset = self._asset + self._asset*(self._position)*(self._get_price()-past_price)/past_price
        # We use `np.clip` to make sure we don't leave the grid

        # An episode is done if the agent has reached the target
        done = np.array_equal(self._day, 360)
        reward = (self._asset-past_asset)/past_asset  # Binary sparse rewards奖励函数
        observation = self._get_obs()
        info = self._get_info()

        # add a frame to the render collection
        # self.renderer.render_step()

        return observation, reward, done, info

    def close(self):
        self.reset()