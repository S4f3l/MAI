import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from tqdm import tqdm


class PrisonersDilemmaEnv:
    def __init__(self):
        self.payoffs = {
            ('C', 'C'): (3, 3),
            ('C', 'D'): (0, 5),
            ('D', 'C'): (5, 0),
            ('D', 'D'): (1, 1)
        }

    def step(self, a1, a2):
        return self.payoffs[(a1, a2)]


class QLearningAgent:
    def __init__(self, learning_rate=0.1, gamma=0.9, epsilon=0.01):
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = {}
        self.actions = ['C', 'D']

    def _ensure_state(self, state):
        if state not in self.q_table:
            self.q_table[state] = {a: 0.0 for a in self.actions}

    def choose_action(self, state):
        self._ensure_state(state)
        if np.random.random() < self.epsilon:
            return np.random.choice(self.actions)
        qvals = self.q_table[state]
        max_val = max(qvals.values())
        best_actions = [a for a, v in qvals.items() if v == max_val]
        return np.random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        self._ensure_state(state)
        self._ensure_state(next_state)
        if done:
            target = reward
        else:
            target = reward + self.gamma * max(self.q_table[next_state].values())
        old_q = self.q_table[state][action]
        self.q_table[state][action] = old_q + self.lr * (target - old_q)


def get_n_episodes(gamma):
    """Адаптивное количество эпизодов - УВЕЛИЧЕНО для высоких γ"""
    if gamma >= 0.99:
        return 80000
    elif gamma >= 0.95:
        return 60000
    elif gamma >= 0.9:
        return 40000
    elif gamma >= 0.7:
        return 25000
    else:
        return 15000


def run_experiment(gamma, n_steps=100, epsilon=0.01, lr=0.1):
    n_episodes = get_n_episodes(gamma)
    print(f"  → Запуск с gamma={gamma}, эпизодов={n_episodes}")

    agent1 = QLearningAgent(learning_rate=lr, gamma=gamma, epsilon=epsilon)
    agent2 = QLearningAgent(learning_rate=lr, gamma=gamma, epsilon=epsilon)

    defection_rates1 = []
    defection_rates2 = []
    first_actions1 = []
    first_actions2 = []

    cooperation_1 = []
    cooperation_2 = []

    for episode in tqdm(range(n_episodes), desc=f"γ={gamma}", leave=False):
        env = PrisonersDilemmaEnv()

        state1 = ('start', 'start')
        state2 = ('start', 'start')

        actions1 = []
        actions2 = []

        for step in range(n_steps):
            a1 = agent1.choose_action(state1)
            a2 = agent2.choose_action(state2)

            actions1.append(a1)
            actions2.append(a2)

            r1, r2 = env.step(a1, a2)

            next_state1 = (a1, a2)
            next_state2 = (a2, a1)

            done = (step == n_steps - 1)

            agent1.update(state1, a1, r1, next_state1, done)
            agent2.update(state2, a2, r2, next_state2, done)

            state1 = next_state1
            state2 = next_state2

        def_rate1 = actions1.count('D') / n_steps
        def_rate2 = actions2.count('D') / n_steps
        defection_rates1.append(def_rate1)
        defection_rates2.append(def_rate2)
        first_actions1.append(actions1[0])
        first_actions2.append(actions2[0])

        if episode % 1000 == 0:
            coop1 = 1 - def_rate1
            coop2 = 1 - def_rate2
            cooperation_1.append(coop1)
            cooperation_2.append(coop2)

    return defection_rates1, defection_rates2, first_actions1, first_actions2, cooperation_1, cooperation_2


print("=== Базовый эксперимент: γ=0.9 ===\n")
deficit1, deficit2, start1, start2, coop1_hist, coop2_hist = run_experiment(gamma=0.9, n_steps=100, epsilon=0.01)

window = 100


def moving_average(data, w):
    if len(data) < w:
        return data
    return np.convolve(data, np.ones(w) / w, mode='valid')


plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
ma1 = moving_average(deficit1, window)
ma2 = moving_average(deficit2, window)
plt.plot(ma1, label='Агент 1')
plt.plot(ma2, label='Агент 2')
plt.xlabel('Эпизод (усреднённый по 100)')
plt.ylabel('Доля дефекций')
plt.title(f'Сходимость доли дефекций (γ=0.9)\nФинальная дефекция: {deficit1[-100:].count(0) / 100:.0%}')
plt.legend()
plt.grid(True)

plt.subplot(1, 2, 2)
episodes_x = list(range(0, get_n_episodes(0.9), 1000))
plt.plot(episodes_x, coop1_hist, label='Агент 1 (кооперация)')
plt.plot(episodes_x, coop2_hist, label='Агент 2 (кооперация)')
plt.xlabel('Эпизод')
plt.ylabel('Доля кооперации')
plt.title('Динамика кооперации в процессе обучения')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('convergence_gamma_09.png', dpi=150)
plt.show()

final_1 = start1[-100:]
final_2 = start2[-100:]
print(f"\n--- Установившаяся стратегия (γ=0.9, последние 100 эпизодов) ---")
print(f"Агент 1: C={final_1.count('C') / 100:.2f}, D={final_1.count('D') / 100:.2f}")
print(f"Агент 2: C={final_2.count('C') / 100:.2f}, D={final_2.count('D') / 100:.2f}")

gamma_values = [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]
results = []

print("\n=== Вариация коэффициента дисконтирования γ ===\n")
for gamma in gamma_values:
    _, _, first1, first2, _, _ = run_experiment(gamma=gamma, n_steps=100, epsilon=0.01)
    final1 = first1[-100:]
    final2 = first2[-100:]
    def1 = final1.count('D') / 100
    def2 = final2.count('D') / 100
    results.append({
        'γ': gamma,
        'Агент 1: % дефекций': def1 * 100,
        'Агент 2: % дефекций': def2 * 100,
        'Средняя дефекция %': (def1 + def2) / 2 * 100
    })
    print(f"γ={gamma}: Агент1={def1 * 100:.1f}%, Агент2={def2 * 100:.1f}%, Среднее={(def1 + def2) / 2 * 100:.1f}%\n")

df_results = pd.DataFrame(results)
print("\n" + df_results.to_string(index=False))

critical_gamma = None
for _, row in df_results.iterrows():
    if row['Средняя дефекция %'] < 80:
        critical_gamma = row['γ']
        break

if critical_gamma:
    print(f"\n✓ Критическое значение γ = {critical_gamma}")
else:
    print("\n✗ Критическое значение γ не достигнуто")

plt.figure(figsize=(10, 6))
plt.plot(df_results['γ'], df_results['Средняя дефекция %'], marker='o', linestyle='-', linewidth=2, markersize=10)
plt.axhline(y=80, color='r', linestyle='--', linewidth=2, label='Порог 80% дефекций')
plt.axhline(y=50, color='orange', linestyle='--', linewidth=2, label='Порог 50% дефекций')
plt.xlabel('Коэффициент дисконтирования γ', fontsize=12)
plt.ylabel('Средняя доля дефекций в конце обучения (%)', fontsize=12)
plt.title('Зависимость установившейся стратегии от γ', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend()
plt.savefig('defection_vs_gamma.png', dpi=150)
plt.show()

df_results.to_csv('strategies_vs_gamma.csv', index=False)
print("\nТаблица стратегий сохранена в strategies_vs_gamma.csv")