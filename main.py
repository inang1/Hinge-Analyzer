import pandas as pd
import matplotlib as plt

class HingeMatches:

    def __init__(self, data_path):
        self.matches = pd.read_json(data_path)

        block_type_list = []
        block_date_list = []
        block_time_list = []
        type_list = []
        like_date_list = []
        like_time_list = []
        like_comment_list = []
        like_type_list = []

        for _ in range(len(self.matches)):
            current_block = self.matches.iloc[_][0]
            if pd.isna(current_block):
                block_type_list.append('NaN')
                block_date_list.append('NaN')
                block_time_list.append('NaN')
                type_list.append('NaN')
            else:
                block_type_list.append(str(current_block[0]['block_type']))
                block_timestamp = str(current_block[0]['timestamp']).split('T')
                block_date_list.append(block_timestamp[0])
                block_time_list.append(block_timestamp[1])
                type_list.append(str(current_block[0]['type']))

            current_like = self.matches.iloc[_][1]
            if pd.isna(current_like):
                like_date_list.append('NaN')
                like_time_list.append('NaN')
                like_comment_list.append('NaN')
                like_type_list.append('NaN')
            else:
                like_timestamp = str(current_like[0]['timestamp']).split('T')
                if len(current_like[0]) == 2:
                    like_date_list.append(like_timestamp[0])
                    like_time_list.append(like_timestamp[1])
                    like_comment_list.append('NaN')
                    like_type_list.append(current_like[0]['type'])
                else:
                    like_date_list.append(like_timestamp[0])
                    like_time_list.append(like_timestamp[1])
                    like_comment_list.append(current_like[0]['comment'])
                    like_type_list.append(current_like[0]['type'])

        self.matches_df = self.matches[['match', 'chats', 'we_met']]
        self.block_like_df = pd.DataFrame([block_type_list, block_date_list, block_time_list, type_list, like_date_list, like_time_list, like_comment_list, like_type_list]).transpose()
        self.block_like_df.columns = ['block_type', 'block_date', 'block_time', 'block_type_type', 'like_date', 'like_time', 'like_comment', 'like_type']
        self.merged = pd.concat([self.block_like_df, self.matches_df], axis=1)

        # Convert Date and Time columns to dt objects
        self.merged['block_date'] = pd.to_datetime(self.merged['block_date'])
        self.merged['block_time'] = pd.to_datetime(self.merged['block_time'])
        self.merged['like_date'] = pd.to_datetime(self.merged['like_date'])
        self.merged['like_time'] = pd.to_datetime(self.merged['like_time'])

        self.merged['block_time'] = self.merged['block_time'].dt.time
        self.merged['like_time'] = self.merged['like_time'].dt.time

        # Add Day of Week column
        self.merged['block_day'] = self.merged['block_date'].dt.strftime('%A')
        self.merged['like_day'] = self.merged['like_date'].dt.strftime('%A')      

        # Reorder columns
        self.merged = self.merged[['block_type', 'block_date', 'block_day', 'block_time', 'block_type_type', 'like_date', 'like_day', 'like_time', 'like_comment', 'like_type', 'match', 'chats', 'we_met']]

hinge_matches = HingeMatches('matches.json')
print(hinge_matches.merged.head())