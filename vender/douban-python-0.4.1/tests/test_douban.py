# encoding: UTF-8

import douban
import testdata

def test_people_entry():
    entry = douban.PeopleEntryFromString(testdata.TEST_PEOPLE_ENTRY)
    assert entry.content.text.startswith("豆瓣寻人")
    assert entry.location.text == "北京"

def test_review_entry():
    entry = douban.ReviewEntryFromString(testdata.TEST_REVIEW_ENTRY)
    assert entry.title.text == "终点之后"
    assert entry.subject.title.text == "Cowboy Bebop"

def test_collection_feed():
    feed = douban.CollectionFeedFromString(testdata.TEST_COLLECTION_FEED)
    assert len(feed.entry) == 3
    
    