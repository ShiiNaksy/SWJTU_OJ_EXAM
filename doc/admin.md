## Exam 管理

### Exam configure 配置（Exam配置文件格式）

*OPTION*

*ExamCharge - post*

Input ->

**`config = {**`

​    `**'start_time': '2021/03/02 09:57:00',**`

​    `**'duration': '02:00:00',**`

​    `**'problem_set_config': [**`

​      `**{**`

​        `**'type': 'select',**`

​        `**'number': 20,**`

​        `**'percentage_tatol': 0.4**`

​        `**},**`

​      `**{**`

​        `**'type': 'fill',**`

​        `**'number': 10,**`

​        `**'percentage_tatol': 0.2**`

​        `**},**`

​      `**{**`

​        `**'type': 'fix',**`

​        `**'number': 10,**`

​        `**'percentage_tatol': 0.2**`

​        `**},**`

​      `**{**`

​        `**'type': 'coding',**`

​        `**'number': 2,**`

​        `**'percentage_tatol': 0.2**`

​        `**},**`

​      `**]**`

  `**}**`

Output -> 

`{'start_time': datetime.datetime(2021, 3, 2, 9, 57), 'end_time': datetime.datetime(2021, 3, 2, 11, 57), 'question_set': {'select': [56, 30, 68, 67, 52, 28, 12, 69, 81, 87, 83, 84, 16, 63, 14, 90, 88,**   **33, 99, 92], 'fill': [330, 323, 383, 340, 365, 318, 367, 322, 310, 363], 'fix': [264, 229, 209, 245, 263, 299, 233, 275, 262, 250], 'coding': [129, 132]}, 'score_config': [{'type': 'select', 'percentage**  **': 0.4}, {'type': 'fill', 'percentage': 0.2}, {'type': 'fix', 'percentage': 0.2}, {'type': 'coding', 'percentage': 0.2}]}**`

在ExamCharge中的PUT部分，应该使用此格式对Exam的config文件进行更改。