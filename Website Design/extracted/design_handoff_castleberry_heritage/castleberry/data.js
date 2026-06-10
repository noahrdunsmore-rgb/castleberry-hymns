/* Castleberry Hymns — mock data drawn from the live app. */

const CB_STATS = {
  uniqueHymns: 168,
  servicesTracked: 68,
  songLeaders: 15,
  trackingSince: 'Jun 2025',
  updated: 'June 3, 2026',
  totalSongs: 892,
  libraries: ['HFWR', 'HFWS', 'eChoice'],
};

const CB_SERVICES = [
  {
    id: 1, date: 'Wed, June 3', dow: 'Wed', d: 'June 3',
    type: 'Wednesday Evening', kind: 'wed', leader: 'Coyte Greer',
    hymns: ['I Know That My Redeemer Lives', 'Why Do You Wait'],
  },
  {
    id: 2, date: 'Sun, May 31', dow: 'Sun', d: 'May 31',
    type: 'Sunday 11:00 AM', kind: 'sun', leader: 'Thomas Holder',
    hymns: ['A Common Love', 'Be Strong and Courageous', 'I Want to Be a Worker', 'We Are One', 'When I Survey the Wondrous Cross'],
  },
  {
    id: 3, date: 'Wed, May 27', dow: 'Wed', d: 'May 27',
    type: 'Wednesday Evening', kind: 'wed', leader: 'Josh Jackson',
    hymns: ['Just As I Am, Without One Plea', 'Take Time to Be Holy'],
  },
  {
    id: 4, date: 'Sun, May 24', dow: 'Sun', d: 'May 24',
    type: 'Sunday 11:00 AM', kind: 'sun', leader: 'Daniel Reyes',
    hymns: ['To God Be the Glory', 'Have Thine Own Way, Lord', 'Sing to Me of Heaven', 'O Sacred Head, Now Wounded'],
  },
  {
    id: 5, date: 'Sun, May 24', dow: 'Sun', d: 'May 24',
    type: 'Sunday 9:30 AM', kind: 'am', leader: 'Mark Hollis',
    hymns: ['Living by Faith', 'Each Step I Take', 'Trust and Obey'],
  },
];

const CB_TOPSONGS = [
  { title: 'To God Be the Glory', count: 24 },
  { title: 'Love Divine, All Loves Excelling', count: 21 },
  { title: 'Jesus, Only Jesus', count: 17 },
  { title: 'Calvary', count: 14 },
  { title: 'Shine, Jesus, Shine', count: 12 },
  { title: 'How Great Thou Art', count: 11 },
  { title: 'Our God, He Is Alive', count: 9 },
];

const CB_PERIODS = ['30 Days', '3 Months', '6 Months', '1 Year', 'All Time'];

const CB_TOPICS = ['Faith', 'Worship', 'Praise', 'Prayer', 'Trust', 'Love', 'Hope', 'Salvation',
  'Commitment', 'Comfort', 'Heaven', 'Encouragement', 'Peace', 'Grace', 'Service',
  "God's Majesty", 'The Cross', 'Community', 'Thanksgiving', "God's Power"];

const CB_LEADERS = ['Coyte Greer', 'Thomas Holder', 'Josh Jackson', 'Daniel Reyes', 'Mark Hollis',
  'Allen Pratt', 'Wesley Kim', 'Caleb Stone'];

// Sample downloader results (shown when a topic/search is active)
const CB_LIBRARY = [
  { title: 'Amazing Grace', lib: 'HFWR', no: 202, topics: ['Grace', 'Salvation'] },
  { title: 'How Great Thou Art', lib: 'HFWS', no: 44, topics: ["God's Majesty", 'Praise'] },
  { title: 'It Is Well with My Soul', lib: 'HFWR', no: 490, topics: ['Peace', 'Trust', 'Comfort'] },
  { title: 'Be Thou My Vision', lib: 'eChoice', no: 118, topics: ['Faith', 'Commitment'] },
  { title: 'Great Is Thy Faithfulness', lib: 'HFWS', no: 71, topics: ['Faith', 'Trust'] },
  { title: 'When I Survey the Wondrous Cross', lib: 'HFWR', no: 315, topics: ['The Cross', 'Worship'] },
  { title: 'Blessed Assurance', lib: 'HFWR', no: 410, topics: ['Hope', 'Salvation'] },
  { title: 'Holy, Holy, Holy', lib: 'HFWS', no: 1, topics: ["God's Majesty", 'Worship'] },
  { title: 'Love Divine, All Loves Excelling', lib: 'HFWR', no: 245, topics: ['Love', 'Grace'] },
  { title: 'Take Time to Be Holy', lib: 'eChoice', no: 388, topics: ['Commitment', 'Prayer'] },
  { title: 'To God Be the Glory', lib: 'HFWR', no: 12, topics: ['Praise', "God's Power"] },
  { title: 'Trust and Obey', lib: 'HFWS', no: 156, topics: ['Trust', 'Faith'] },
];

Object.assign(window, { CB_STATS, CB_SERVICES, CB_TOPSONGS, CB_PERIODS, CB_TOPICS, CB_LEADERS, CB_LIBRARY });
