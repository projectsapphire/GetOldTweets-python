# -*- coding: utf-8 -*-
import sys,getopt,datetime,codecs
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main(argv):

	if len(argv) == 0:
		print('You must pass some parameters. Use \"-h\" to help.')
		return

	if len(argv) == 1 and argv[0] == '-h':
		f = open('exporter_help_text.txt', 'r')
		print f.read()
		f.close()

		return

	try:
		opts, args = getopt.getopt(argv, "", ("username=", "near=", "within=", "since=", "until=", "querysearch=", "toptweets", "maxtweets=", "output=", "author_list_id="))

		tweetCriteria = got.manager.TweetCriteria()
		outputFileName = "output_got.csv"
		outputFile = None
		author_list_id = ""

		for opt,arg in opts:
			if opt == '--username':
				tweetCriteria.username = arg

			elif opt == '--since':
				tweetCriteria.since = arg

			elif opt == '--until':
				tweetCriteria.until = arg

			elif opt == '--querysearch':
				tweetCriteria.querySearch = arg

			elif opt == '--toptweets':
				tweetCriteria.topTweets = True

			elif opt == '--maxtweets':
				tweetCriteria.maxTweets = int(arg)
			
			elif opt == '--near':
				tweetCriteria.near = '"' + arg + '"'
			
			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--within':
				tweetCriteria.within = '"' + arg + '"'

			elif opt == '--output':
				outputFileName = arg
			
			elif opt == '--author_list_id':
				author_list_id = arg
		
		if author_list_id == "":
			print("Please specify the author_list_id")
			return
				
		outputFile = codecs.open(outputFileName, "w+", "utf-8")

		# outputFile.write('username;date;retweets;favorites;text;geo;mentions;hashtags;id;permalink;expanded_url')

		print('Searching...\n')

		def receiveBuffer(tweets):
			import json
			outputFile.write("[")
			for t in tweets:
				twet = {
					"id"           : t.id,
					"created_at"   : str(t.date.strftime("%Y-%m-%d %H:%M")),
					"text"		   : t.text,
					"entities"     : {
						"urls":[
							{
								"url":t.url,
								"expanded_url":t.expanded_url,
								"display_url" : t.display_url
							}
						]
					},
					"retweet_count": t.retweets,
					"favorite_count": t.favorites,
					"user":{
						"screen_name":t.username
					},
					"author_list_id": author_list_id
				}
				outputFile.write(json.dumps(twet, ensure_ascii=False) + ",")
				# outputFile.write(('\n%s;%s;%d;%d;"%s";%s;%s;%s;"%s";%s;%s' % (t.username, t.date.strftime("%Y-%m-%d %H:%M"), t.retweets, t.favorites, t.text, t.geo, t.mentions, t.hashtags, t.id, t.permalink, t.expanded_url)))
			outputFile.write("]")
			outputFile.flush()
			print('More %d saved on file...\n' % len(tweets))

		got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

	except arg:
		print('Arguments parser error, try -h' + arg)
	finally:
		if outputFile:
			outputFile.close()
		print('Done. Output file generated "%s".' % outputFileName)

if __name__ == '__main__':
	main(sys.argv[1:])
