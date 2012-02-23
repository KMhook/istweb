# encoding: UTF-8

"""Support data for tests."""

TEST_PEOPLE_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:gd="http://schemas.google.com/g/2005" xmlns:opensearch="http://a9.com/-/spec/opensearchrss/1.0/" xmlns:db="http://www.douban.com/xmlns/">
    <db:location>北京</db:location>
    <title>hongqn</title>
    <content>豆瓣寻人: 网站开发和设计人员
http://blog.douban.com/douban/2007/01/11/78/
</content>
    <link rel="self" href="http://api.douban.com/people/1002211"/>
    <link rel="alternate" href="http://www.douban.com/people/1002211/"/>
    <link rel="icon" href="http://www.douban.com/icon/u1002211.jpg"/>

    <id>http://api.douban.com/people/hongqn</id>
</entry>"""


TEST_REVIEW_ENTRY = """<?xml version="1.0" encoding="UTF-8"?>
<entry xmlns="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/" xmlns:gd="http://schemas.google.com/g/2005" xmlns:opensearch="http://a9.com/-/spec/opensearchrss/1.0/">
    <id>http://api.douban.com/review/1138468</id>
    <title>终点之后</title>
    <author>
        <link href="http://api.douban.com/people/iserlohnwind" rel="self"/>
        <link href="http://www.douban.com/people/iserlohnwind/" rel="alternate"/>
        <link href="http://www.douban.com/icon/u1360856.jpg" rel="icon"/>
        <name>伊谢尔伦的风</name>

        <uri>http://api.douban.com/people/1360856</uri>
    </author>
    <updated>2007-03-27T08:54:43+08:00</updated>
    <link href="http://api.douban.com/review/1138468" rel="self"/>
    <link href="http://www.douban.com/review/1138468/" rel="alternate"/>
    <link href="http://api.douban.com/movie/subject/1424406" rel="http://www.douban.com/2007#subject"/>
    <summary>我还是忍不住要说菲。 
　　 
渡边唯一的仁慈，是让小鬼艾德带走了小狗爱因，然后大人们就一步步开始了清醒的葬送：斯派克一往无前义无反顾，杰特明白老搭档的臭脾气所以沉默不语，而当时的菲原本已经是第二次不辞而别——“因为分别太难受了，所以我一个人走了。”《杂烩武士》里15岁的风这样告诉仁和无幻——可又找不到回去的地方，终于还是把自己扔给了BEBOP号，却被告知终曲即将奏响。然而菲不是风，她能悠然...</summary>

    <gd:rating max="5" min="1" value="4"/>
    <db:subject>
        <id>http://api.douban.com/movie/subject/1424406</id>
        <title>Cowboy Bebop</title>
        <category scheme="http://www.douban.com/2007#kind" term="http://www.douban.com/2007#movie"/>
        <author>
            <name>渡边信一郎</name>

        </author>
        <link href="http://api.douban.com/movie/subject/1424406" rel="self"/>
        <link href="http://www.douban.com/subject/1424406/" rel="alternate"/>
        <link href="http://otho.douban.com/spic/s2351152.jpg" rel="image"/>
        <db:attribute name="pubdate">1998</db:attribute>
        <db:attribute name="language">日语</db:attribute>
        <db:attribute name="website">http://www.cowboybebop.org/</db:attribute>

        <db:attribute lang="zh_CN" name="aka">赏金猎人</db:attribute>
        <db:attribute name="imdb">http://www.imdb.com/title/tt0213338/</db:attribute>
        <db:attribute name="country">Japan</db:attribute>
        <db:attribute name="cast">山寺宏一</db:attribute>
        <db:attribute name="cast">石塚运昇</db:attribute>
        <db:attribute name="cast">林原惠</db:attribute>

    </db:subject>
</entry>
"""

TEST_COLLECTION_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:db="http://www.douban.com/xmlns/" xmlns:gd="http://schemas.google.com/g/2005" xmlns:opensearch="http://a9.com/-/spec/opensearchrss/1.0/">
	<title>阿北 的收藏</title>
	<author>
		<link href="http://api.douban.com/people/ahbei" rel="self"/>
		<link href="http://www.douban.com/people/ahbei/" rel="alternate"/>
		<link href="http://www.douban.com/icon/u1000001.jpg" rel="icon"/>
		<name>阿北</name>
		<uri>http://api.douban.com/people/1000001</uri>
	</author>
	<opensearch:startIndex>1</opensearch:startIndex>
	<opensearch:itemPerPage>10</opensearch:itemPerPage>
	<opensearch:totalResults>106</opensearch:totalResults>
	<entry>
		<id>http://api.douban.com/people/1000001/collection/22588658</id>
		<title>读过 比我老的老头</title>
		<updated>2007-12-28T18:11:38+08:00</updated>
		<db:status>read</db:status>
		<db:subject>
			<id>http://api.douban.com/book/subject/1049361</id>
			<title>比我老的老头</title>
			<category scheme="http://www.douban.com/2007#kind" term="http://www.douban.com/2007#book"/>
			<author>
				<name>黄永玉</name>
			</author>
			<link href="http://api.douban.com/book/subject/1049361" rel="self"/>
			<link href="http://www.douban.com/subject/1049361/" rel="alternate"/>
			<link href="http://otho.douban.com/spic/s1845564.jpg" rel="image"/>
			<db:attribute name="isbn10">7506326302</db:attribute>
			<db:attribute name="isbn13">9787506326308</db:attribute>
			<db:attribute name="price">23</db:attribute>
			<db:attribute name="author">黄永玉</db:attribute>
			<db:attribute name="publisher">作家出版社</db:attribute>
			<db:attribute name="pubdate">2003-7-1</db:attribute>
		</db:subject>
	</entry>
	<entry>
		<id>http://api.douban.com/people/1000001/collection/18565656</id>
		<title>在读 Crossing the Chasm</title>
		<updated>2007-08-13T10:37:32+08:00</updated>
		<db:status>reading</db:status>
		<db:subject>
			<id>http://api.douban.com/book/subject/1431653</id>
			<title>Crossing the Chasm</title>
			<category scheme="http://www.douban.com/2007#kind" term="http://www.douban.com/2007#book"/>
			<author>
				<name>Geoffrey A. Moore</name>
			</author>
			<link href="http://api.douban.com/book/subject/1431653" rel="self"/>
			<link href="http://www.douban.com/subject/1431653/" rel="alternate"/>
			<link href="http://otho.douban.com/spic/s1445449.jpg" rel="image"/>
			<db:attribute name="isbn10">0060517123</db:attribute>
			<db:attribute name="isbn13">9780060517120</db:attribute>
			<db:attribute name="publisher">Collins</db:attribute>
			<db:attribute name="author">Geoffrey A. Moore</db:attribute>
			<db:attribute name="price">USD 17.95</db:attribute>
			<db:attribute name="pubdate">2002-08</db:attribute>
		</db:subject>
		<db:tag name="商业"/>
	</entry>
	<entry>
		<id>http://api.douban.com/people/1000001/collection/16613855</id>
		<title>想读 The Ants</title>
		<updated>2007-07-04T23:56:32+08:00</updated>
		<db:status>wish</db:status>
		<db:subject>
			<id>http://api.douban.com/book/subject/2139542</id>
			<title>The Ants</title>
			<category scheme="http://www.douban.com/2007#kind" term="http://www.douban.com/2007#book"/>
			<author>
				<name>Bert Hölldobler</name>
			</author>
			<author>
				<name>Edward O. Wilson</name>
			</author>
			<link href="http://api.douban.com/book/subject/2139542" rel="self"/>
			<link href="http://www.douban.com/subject/2139542/" rel="alternate"/>
			<link href="http://otho.douban.com/spic/s2579256.jpg" rel="image"/>
			<db:attribute name="isbn10">3540520929</db:attribute>
			<db:attribute name="isbn13">9783540520924</db:attribute>
			<db:attribute name="author">Bert Hölldobler</db:attribute>
			<db:attribute name="author">Edward O. Wilson</db:attribute>
			<db:attribute name="price">USD 209.00</db:attribute>
			<db:attribute name="publisher">Springer</db:attribute>
			<db:attribute name="pubdate">1998-09-07</db:attribute>
		</db:subject>
	</entry>
</feed>
"""