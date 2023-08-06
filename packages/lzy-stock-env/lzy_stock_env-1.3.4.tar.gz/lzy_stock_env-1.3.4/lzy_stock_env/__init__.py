from gym.envs.registration import register

register(
    id='lzy_stock_env-v0',
    entry_point='lzy_stock_env.envs:LzyEnv',
    max_episode_steps=1000,
)