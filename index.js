import Twitter from 'twitter';
import { Client } from '@notionhq/client';
import { NOTION_KEY, ART_INSPO_DB_ID, twitter_creds } from './creds.js';

const notion = new Client({ auth: NOTION_KEY });

const databaseId = ART_INSPO_DB_ID;

var twitter = new Twitter(twitter_creds);

var params = { id: '1415337129446567938' };
twitter.get('statuses/show', params, function (error, tweets, response) {
  if (!error) {
    console.log(tweets);
  } else {
    console.log(error);
  }
});

async function addItem(text) {
  try {
    await notion.request({
      path: 'pages',
      method: 'POST',
      body: {
        parent: { database_id: databaseId },
        properties: {
          title: {
            title: [
              {
                text: {
                  content: text,
                },
              },
            ],
          },
        },
      },
    });
    console.log('Success! Entry added.');
  } catch (error) {
    console.error(error.body);
  }
}

//addItem('Yurts in Big Sur, California');
