#---------------------------------------------
# File name: test_nlpCalls.py
# Description: pytest file for nlpCalls
# Author: Gilbert Yap (gilberty@bu.edu)
# Date: October 29, 2020
#---------------------------------------------

import helper, nlpCalls
import pytest, sys

sample_text = u'I am thinking about taking a short trip to Revere Beach, but I get sunburn very easily. Maybe I should instead visit Castle Island with Gilbert. I heard that sunset there is really beautiful!'

def test_nlpCalls():
    (client, errors) = nlpCalls.init_google_nlp()
    if client is None:
        helper.print_errors(errors)
        pytest.raises(SystemExit)
        sys.exit(1)
    helper.console_print('Authentication succeeded')
    
    # The text to analyze
    (sentimentDict,errors) = nlpCalls.analyze_text_sentiment(client, sample_text)
    if len(sentimentDict) == 0:
        helper.print_errors(errors)
        sys.exit(1)

    helper.console_print('Text: {}'.format(sample_text))
    helper.console_print('Sentiment: {}, {}'.format(sentimentDict['score'], sentimentDict['magnitude']))

    assert sentimentDict['score'] == pytest.approx(0.0)
    assert sentimentDict['magnitude'] == pytest.approx(1.8)

if __name__ == '__main__':
    test_nlpCalls()
    sys.exit(0)