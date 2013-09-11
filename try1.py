
import math
import json
import sys



def tag_list( post_dict, corp_prob ):
    '''
    '''
    count = 0
    for word in post_dict:
        count += post_dict[word]

    post_prob = {}
    pair = []
    for word in post_dict:
        value = float(post_dict[word]) / count
        post_prob[word] = value
        if value > 1.0 or value < 0.0:
            print("LOCAL WTF!!!!!!")
        score = pmi(value, corp_prob[word])
        pair.append( (score,word) )

    #print sorted(pair, reverse = True)[:5]

    return sorted(pair, reverse = True)[:5]

def pmi( pxy, px, py = 1):
    '''
    '''
    #print (pxy,px,py)
    return math.log( float(pxy) / ( px * py ) )

def reduce_word(word):
    minimal = (((word.lower()
              ).replace("<p>","")
              ).replace("</p>","")
              ).strip('!@#$%^&*()<>?:\"{}|,./;\'[]\\')
              )
    return minimal

def good_words(words):
    '''
    '''
    long_words = []
    #print words

    for each in words:
        word = reduce_word(each)
        if len(word) > 1:
            long_words.append( word )
    #print long_words

    return long_words

def term_dict(words):
    '''
    (list of words) -> dictionary term:frequency
    '''
    term_freq = {}

    for each in words:
        if term_freq.has_key(each):
            term_freq[each] +=1
        else:
            term_freq[each] = 1
    return term_freq

def update_corpus(loc_dict, glob_dict):
    '''
    '''
    for word in loc_dict:
        if glob_dict.has_key(word):
            glob_dict[word] +=1
        else:
            glob_dict[word] = 1

    return glob_dict

def main(filename):

    post_list = []
    corp_dict = {}

    with open(filename) as jsonfile:
        for line in jsonfile:
            post = json.loads(line)
            body = post["Body"]
            title = post["Title"]
            tags = post["Tags"]
            words = body.split() + title.split()

            loc_word_freq = term_dict( good_words(words) )
            post_list.append( (loc_word_freq,tags) )

            corp_dict = update_corpus(loc_word_freq, corp_dict)

    count = 0
    for word in corp_dict:
        count += corp_dict[word]
        if corp_dict[word] > 30:
            print( word, corp_dict[word] )
    print count

    corp_prob = {}
    for word in corp_dict:
        value = float(corp_dict[word]) / count
        corp_prob[word] = value
        if value > 1.0 or value < 0.0:
            print("WTF!!!!!!!!!!!!")

    i = 0
    gtp = 0
    gfp = 0
    gfn = 0
    for post in post_list:
        top_tags = tag_list( post[0], corp_prob )

        tp = 0
        fp = 0
        real_tags = post[1].split()
        #print "Real Tags: ", real_tags
        #print "Top Tags:  ", top_tags

        for my_tag in top_tags:
            if my_tag[1] in real_tags:
                tp +=1
                real_tags.remove(my_tag[1])
            else:
                fp +=1
            fn = len(real_tags)
        print
        print post[1]
        print tp,fp,fn
        gtp += tp
        gfp += fp
        gfn += fn
        print

        #i += 1
        #if i > 5: break

    print metric(gtp, gfp, gfn)
def metric(tp,fp,fn):
    '''
    '''
    p = float(tp) / (tp + fp)
    r = float(tp) / (tp + fn)
    return 2*r*p/(r+p)

if __name__ == "__main__":
    main(sys.argv[1])
