import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import seaborn as sns

voting_data = pd.read_csv('vote.csv')
age_data = pd.read_csv('age.csv', encoding='utf-8')

merged_data = pd.merge(voting_data, age_data, left_on=['구', '읍면동명'], right_on=['시군구명', '읍면동명'], how='left')
grouped_by_district = merged_data.groupby('구').agg({'투표수': 'sum', '선거인수': 'sum'})
grouped_by_district['투표율'] = grouped_by_district['투표수'] / grouped_by_district['선거인수'] * 100

merged_data['weighted_age'] = merged_data['투표수'] * merged_data['전체 평균연령']
age_by_district = merged_data.groupby('구').agg({'weighted_age': 'sum', '투표수': 'sum'})
age_by_district['average_voting_age'] = age_by_district['weighted_age'] / age_by_district['투표수']

candidate_columns = ['박영선','오세훈','허경영','이수봉','배영규','김진아','송명숙','정동희','이도엽','신지예']  # Replace with actual candidate columns
votes_per_candidate = merged_data.groupby('구')[candidate_columns].sum()
total_votes_per_district = votes_per_candidate.sum(axis=1)
for candidate in candidate_columns:
    votes_per_candidate[candidate + '_share'] = votes_per_candidate[candidate] / total_votes_per_district * 100
vote_shares = votes_per_candidate[[col + '_share' for col in candidate_columns]]

fig, axes = plt.subplots(3, 1, figsize=(10, 18))

grouped_by_district['투표율'].sort_values().plot(kind='barh', ax=axes[0], color='skyblue')
axes[0].set_title('Voter Turnout by District (%)')
axes[0].set_xlabel('Turnout (%)')

age_by_district['average_voting_age'].sort_values().plot(kind='barh', ax=axes[1], color='lightgreen')
axes[1].set_title('Average Voting Age by District')
axes[1].set_xlabel('Average Age')

sns.heatmap(vote_shares.T, annot=True, fmt=".1f", linewidths=.5, ax=axes[2], square=True, cmap='viridis')
axes[2].set_title('Candidate Vote Share by District (%)')
axes[2].set_xlabel('District')
axes[2].set_ylabel('Candidate')

plt.tight_layout()
plt.show()