import gym
from DDPG.actor_critic import ActorCritic
from DDPG.replaybuffer import ReplayBuffer
import numpy as np

BUFFER_SIZE = 100000
BATCH_SIZE = 32
GAMMA = 0.9
episode_count = 2000


def run():
    env = gym.make('CartPole-v1')

    action_dim = env.action_space.n
    state_dim = env.observation_space.shape[0]

    actor_critic = ActorCritic(state_dim, action_dim)
    actor = actor_critic.actor
    actor_target = actor_critic.actor_target
    critic = actor_critic.critic
    critic_target = actor_critic.critic_target
    buffer = ReplayBuffer(BUFFER_SIZE)

    # Now load the weight
    print("Now we load the weight") #TODO: change to checkpoints
    try:
        actor.model.load_weights("actormodel.h5")
        actor_target.model.load_weights("actormodel.h5")
        critic.model.load_weights("criticmodel.h5")
        critic_target.model.load_weights("criticmodel.h5")
        print("Weight load successfully")
    except:
        print("Cannot find the weight")

    for i in range(episode_count):
        print("Episode : " + str(i) + " Replay Buffer " + str(buffer.count()))

        obs = env.reset()
        episode_rewards = 0
        done = False
        while not done:
            actions_prob = actor.model.predict([obs])
            #TODO: take action with a certain probability
            action = np.random.choice(list(range(action_dim)), 1, p=actions_prob)[0]
            new_obs, reward, done, info = env.step(action)

            buffer.add(obs, action, reward, new_obs, done)  # Add replay buffer

            # Do the batch update TODO:make faster
            batch = buffer.getBatch(BATCH_SIZE)
            states = np.asarray([e[0] for e in batch])
            actions = np.asarray([e[1] for e in batch])
            rewards = np.asarray([e[2] for e in batch])
            new_states = np.asarray([e[3] for e in batch])
            dones = np.asarray([e[4] for e in batch])
            y_t = np.asarray([e[1] for e in batch])

            target_q_values = critic.target_model.predict([new_states, actor_target.model.predict(new_states)])

            for k in range(len(batch)):
                if dones[k]:
                    y_t[k] = rewards[k]
                else:
                    y_t[k] = rewards[k] + GAMMA * target_q_values[k]