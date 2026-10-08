import json
import matplotlib.pyplot as plt
from scipy import stats

with open("all.jsonl", "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

print("Number of records:", len(data))


# Check for missing human or ChatGPT answers
missing_human = 0
missing_chatgpt = 0

for record in data:
    if not record["human_answers"]:
        missing_human += 1
    if not record["chatgpt_answers"]:
        missing_chatgpt += 1  

print("Missing human answers:", missing_human)
print("Missing ChatGPT answers:", missing_chatgpt) 


# Counting useful records (records with both human and ChatGPT answers)
useful_records = 0

for record in data:
    if record["human_answers"] and record["chatgpt_answers"]:
        useful_records += 1
        
print("Number of useful records:", useful_records)


# Counting average response lengths for human and ChatGPT answers
human_response_lengths = []
chatgpt_response_lengths = []

for record in data:
    if record["human_answers"] and record["chatgpt_answers"]:
        human_response_lengths.append(len(record["human_answers"][0].split()))
        chatgpt_response_lengths.append(len(record["chatgpt_answers"][0].split()))

print("Average human response length:", sum(human_response_lengths) / len(human_response_lengths) if human_response_lengths else 0)
print("Average ChatGPT response length:", sum(chatgpt_response_lengths) / len(chatgpt_response_lengths) if chatgpt_response_lengths else 0)


# Visualizing the distribution of response lengths
plt.hist([human_response_lengths, chatgpt_response_lengths], label = ["Human", "ChatGPT"], alpha = 0.5, bins = 50, range=(0, 500))
plt.xlabel("Number of Words")
plt.ylabel("Frequency")
plt.title("Distribution of Response Lengths")
plt.legend()

plt.show()


# Calculating average response length differences between human and ChatGPT responses for each question
diff_list = []
for question in range(len(human_response_lengths)):
    diff_list.append(chatgpt_response_lengths[question] - human_response_lengths[question])

print("Average response length difference:", sum(diff_list) / len(diff_list) if diff_list else 0)


# Checking for statistical significance of mean of these differences using a t-test
print(stats.ttest_1samp(diff_list, 0))


# Calculating and comparing the number of sentences in human and ChatGPT responses
human_sentence_counts = []
chatgpt_sentence_counts = []

for record in data:
    if record["human_answers"] and record["chatgpt_answers"]:
        human_sentence_counts.append(record["human_answers"][0].count('.') + record["human_answers"][0].count('!') + record["human_answers"][0].count('?'))
        chatgpt_sentence_counts.append(record["chatgpt_answers"][0].count(".") + record["chatgpt_answers"][0].count("!") + record["chatgpt_answers"][0].count("?"))

print("Average human sentence count:", sum(human_sentence_counts) / len(human_sentence_counts) if human_sentence_counts else 0)
print("Average ChatGPT sentence count:", sum(chatgpt_sentence_counts) / len(chatgpt_sentence_counts) if chatgpt_sentence_counts else 0)


#  Calculating average sentence count differences between human and ChatGPT responses for each question
sentence_diff_list = []

for sentence in range(len(human_sentence_counts)):
    sentence_diff_list.append(chatgpt_sentence_counts[sentence] - human_sentence_counts[sentence])

print("Average sentence count difference:", sum(sentence_diff_list) / len(sentence_diff_list) if sentence_diff_list else 0)


# Checking for statistical significance of mean of these differences in sentence counts using a t-test
print(stats.ttest_1samp(sentence_diff_list, 0))


# Calculating the average number of words per sentence for human and ChatGPT responses
human_average_sentence_lengths = []
chatgpt_average_sentence_lengths = []

for i in range(len(human_response_lengths)):
    human_average_sentence_lengths.append(human_response_lengths[i]/human_sentence_counts[i] if human_sentence_counts[i] != 0 else 0)
    chatgpt_average_sentence_lengths.append(chatgpt_response_lengths[i]/chatgpt_sentence_counts[i] if chatgpt_sentence_counts[i] != 0 else 0)

print("Average human words per sentence:", sum(human_average_sentence_lengths) / len(human_average_sentence_lengths) if human_average_sentence_lengths else 0)
print("Average ChatGPT words per sentence:", sum(chatgpt_average_sentence_lengths) / len(chatgpt_average_sentence_lengths) if chatgpt_average_sentence_lengths else 0)


# Calculating average words per sentence differences between human and ChatGPT responses for each question
words_per_sentence_diff_list = []

for i in range(len(human_average_sentence_lengths)):
    words_per_sentence_diff_list.append(chatgpt_average_sentence_lengths[i] - human_average_sentence_lengths[i])

print("Average words per sentence difference:", sum(words_per_sentence_diff_list) / len(words_per_sentence_diff_list) if words_per_sentence_diff_list else 0)


# Checking for statistical significance of mean of these differences in words per sentence using a t-test
print(stats.ttest_1samp(words_per_sentence_diff_list, 0))


# Calculating TTR (Type-Token Ratio) for human and ChatGPT responses
human_ttr_list = []
chatgpt_ttr_list = []

for record in data:
    if record["human_answers"] and record["chatgpt_answers"]:
        if len(record["human_answers"][0].split()) > 0 and len(record["chatgpt_answers"][0].split()) > 0:
            human_ttr_list.append(len(set(record["human_answers"][0].lower().split()))/len(record["human_answers"][0].split()))
            chatgpt_ttr_list.append(len(set(record["chatgpt_answers"][0].lower().split()))/len(record["chatgpt_answers"][0].split()))

print("Average human TTR:", sum(human_ttr_list) / len(human_ttr_list) if human_ttr_list else 0)
print("Average ChatGPT TTR:", sum(chatgpt_ttr_list) / len(chatgpt_ttr_list) if chatgpt_ttr_list else 0)


# Calculating average TTR differences between human and ChatGPT responses for each question
ttr_diff_list = []

for i in range(len(human_ttr_list)):
    ttr_diff_list.append(chatgpt_ttr_list[i] - human_ttr_list[i])

print("Average TTR difference:", sum(ttr_diff_list) / len(ttr_diff_list) if ttr_diff_list else 0)


# Checking for statistical significance of mean of these differences in TTR using a t-test
print(stats.ttest_1samp(ttr_diff_list, 0))


# Analyzing punctuation patterns in human and ChatGPT responses
human_punctuation_counts = []
chatgpt_punctuation_counts = []

for record in data:
    if record["human_answers"] and record["chatgpt_answers"]:
        human_punctuation_counts.append(sum(record["human_answers"][0].count(p) for p in ['.', '!', '?', ',', ';', ':']))
        chatgpt_punctuation_counts.append(sum(record["chatgpt_answers"][0].count(p) for p in ['.', '!', '?', ',', ';', ':']))

print("Average human punctuation count:", sum(human_punctuation_counts) / len(human_punctuation_counts) if human_punctuation_counts else 0)
print("Average ChatGPT punctuation count:", sum(chatgpt_punctuation_counts) / len(chatgpt_punctuation_counts) if chatgpt_punctuation_counts else 0)


# Analyzing punctuation pattern per 100 words in human and ChatGPT responses
human_punctuation_per_100 = []
chatgpt_punctuation_per_100 = []

for i in range(len(human_response_lengths)):
    if human_response_lengths[i] > 0:
        human_punctuation_per_100.append((human_punctuation_counts[i] / human_response_lengths[i]) * 100)
    else:
        human_punctuation_per_100.append(0)

    if chatgpt_response_lengths[i] > 0:
        chatgpt_punctuation_per_100.append((chatgpt_punctuation_counts[i] / chatgpt_response_lengths[i]) * 100)
    else:
        chatgpt_punctuation_per_100.append(0)

print("Average human punctuation per 100 words:", sum(human_punctuation_per_100) / len(human_punctuation_per_100) if human_punctuation_per_100 else 0)
print("Average ChatGPT punctuation per 100 words:", sum(chatgpt_punctuation_per_100) / len(chatgpt_punctuation_per_100) if chatgpt_punctuation_per_100 else 0)


# Calculating average punctuation per 100 words differences between human and ChatGPT responses for each question
punctuation_per_100_diff_list = []

for i in range(len(human_punctuation_per_100)):
    punctuation_per_100_diff_list.append(chatgpt_punctuation_per_100[i] - human_punctuation_per_100[i])

print("Average punctuation per 100 words difference:", sum(punctuation_per_100_diff_list) / len(punctuation_per_100_diff_list) if punctuation_per_100_diff_list else 0)


# Checking for statistical significance of mean of these differences in punctuation per 100 words using a t-test
print(stats.ttest_1samp(punctuation_per_100_diff_list, 0))


# Visualizing the difference of response lengths between human and ChatGPT responses
labels = ['Human', 'ChatGPT']
values = [sum(human_response_lengths) / len(human_response_lengths) if human_response_lengths else 0, sum(chatgpt_response_lengths) / len(chatgpt_response_lengths) if chatgpt_response_lengths else 0]

plt.bar(labels, values, color=['blue', 'orange'])
plt.bar_label(plt.gca().containers[0]) 
plt.ylabel('Average Response Length (words)')
plt.title('Average Response Length Comparison')
plt.show()


# Visualizing the difference of sentence counts between human and ChatGPT responses
labels = ['Human', 'ChatGPT']
values = [sum(human_sentence_counts) / len(human_sentence_counts) if human_sentence_counts else 0, sum(chatgpt_sentence_counts) / len(chatgpt_sentence_counts) if chatgpt_sentence_counts else 0]

plt.bar(labels, values, color=['blue', 'orange'])
plt.bar_label(plt.gca().containers[0])
plt.ylabel('Average Sentence Count')
plt.title('Average Sentence Count Comparison')
plt.show()


# Visualizing the difference of words per sentence between human and ChatGPT responses
labels = ['Human', 'ChatGPT']
values = [sum(human_average_sentence_lengths) / len(human_average_sentence_lengths) if human_average_sentence_lengths else 0, sum(chatgpt_average_sentence_lengths) / len(chatgpt_average_sentence_lengths) if chatgpt_average_sentence_lengths else 0]

plt.bar(labels, values, color=['blue', 'orange'])
plt.bar_label(plt.gca().containers[0])
plt.ylabel('Average Words per Sentence')
plt.title('Average Words per Sentence Comparison')
plt.show()


# Visualizing the difference of TTR between human and ChatGPT responses
labels = ['Human', 'ChatGPT']
values = [sum(human_ttr_list) / len(human_ttr_list) if human_ttr_list else 0, sum(chatgpt_ttr_list) / len(chatgpt_ttr_list) if chatgpt_ttr_list else 0]

plt.bar(labels, values, color=['blue', 'orange'])
plt.bar_label(plt.gca().containers[0])
plt.ylabel('Average TTR')
plt.title('Average TTR Comparison')
plt.show()


# Visualizing the difference of punctuation per 100 words between human and ChatGPT responses
labels = ['Human', 'ChatGPT']
values = [sum(human_punctuation_per_100) / len(human_punctuation_per_100) if human_punctuation_per_100 else 0, sum(chatgpt_punctuation_per_100) / len(chatgpt_punctuation_per_100) if chatgpt_punctuation_per_100 else 0]

plt.bar(labels, values, color=['blue', 'orange'])
plt.bar_label(plt.gca().containers[0])
plt.ylabel('Average Punctuation per 100 Words')
plt.title('Average Punctuation per 100 Words Comparison')
plt.show()