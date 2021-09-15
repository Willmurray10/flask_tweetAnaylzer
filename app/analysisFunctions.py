import textblob, nltk, syllables, math
nltk.download('popular')

failure_message = "Sorry, we could not provide this statistic"

def avg_likes(likes):
    try:
        likes_avg = sum(likes) / len(likes)
        return likes_avg

    except:
        return failure_message

def avg_RT(retweets):
    try:
        rt_avg = sum(retweets) / len(retweets)
        return rt_avg

    except:
        return failure_message

def tweet_charavg(tweets):
    try:
    #textblob words remove punctuations/spaces, twitter includes
        words = []
        char_sum = 0
        for i in range(0, len(tweets)-1):
            temp_blob = textblob.TextBlob(tweets[i])
            for word in temp_blob.words:
                words.append(word)
        for word in words:
            char_sum+=1
            for i in word:
                char_sum +=1
        char_avg = char_sum / len(tweets)
        return char_avg

    except:
        return failure_message

def tweet_wordavg(tweets):
    try:
        word_sum = 0
        for i in range(0, len(tweets)-1):
            temp_blob = textblob.TextBlob(tweets[i])
            for word in temp_blob.words:
                word_sum +=1
        
        word_avg = word_sum / len(tweets)
        return word_avg

    except:
        return failure_message

def polarity_analysis(tweets):
    try:
        pol_sum = 0
        for i in range(0, len(tweets)-1):
            temp_blob = textblob.TextBlob(tweets[i])
            temp_pol = temp_blob.polarity
            pol_sum += temp_pol
            
        pol_avg = pol_sum / len(tweets)
        return pol_avg

    except:
        return failure_message

def subjectivity_analysis(tweets):
    try:
        subj_sum = 0
        for i in range(0, len(tweets)-1):
            temp_blob = textblob.TextBlob(tweets[i])
            temp_subj = temp_blob.subjectivity
            subj_sum += temp_subj

        subj_avg = subj_sum / len(tweets)
        return subj_avg
    except:
        return failure_message
    
def fkgl_analysis(tweets):
    #fkgl_formula = 0.39*(total_words/total_sentences) + 11.8*(total_syllables/total_words)-15.59
    try:
        fkgl_scores = []
        fkgl_finalscore = 0

        for i in range(0, len(tweets)-1):
            word_sum = 0
            sentence_sum = 0
            syllable_sum = 0
            temp_blob = textblob.TextBlob(tweets[i])
            for sentence in temp_blob.sentences:
                sentence_sum += 1
            for word in temp_blob.words:
                word_sum += 1
                num_syllables = syllables.estimate(word)
                syllable_sum += num_syllables

            fkgl = 0.39 * (word_sum / sentence_sum) + 11.8 * (syllable_sum / word_sum) - 15.59
            fkgl_scores.append(fkgl)

        fkgl_finalscore = sum(fkgl_scores) / len(tweets)
        return fkgl_finalscore
    
    except:
        return failure_message

def smog_analysis(tweets):
    #smog_formula = 1.043 * math.sqrt(polysyllable_sum * (30 / sentence_sum)) + 3.1291
    try:
        smog_scores = []
        sentence_sum = 0
        polysyllable_sum = 0

        for i in range(0, len(tweets)-1):
            temp_blob = textblob.TextBlob(tweets[i])
            for sentence in temp_blob.sentences:
                sentence_sum += 1
            for word in temp_blob.words:
                num_syllables = syllables.estimate(word)
                if num_syllables >= 3:
                    polysyllable_sum +=1
            smog= 1.043 * math.sqrt(polysyllable_sum * (30 / sentence_sum)) + 3.1291
            smog_scores.append(smog)

        smog_finalscore = sum(smog_scores) / len(tweets)
        return smog_finalscore
    
    except:
        return failure_message