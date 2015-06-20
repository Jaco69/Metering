<?php
/**
 * Export to PHP Array plugin for PHPMyAdmin
 * @version 0.2b
 */

//
// Database `emoncms`
//

// `emoncms`.`dashboard`
$dashboard = array(
  array('id' => '1','userid' => '1','content' => '<div pricekwh="0.21" currency="Eur" kwhd="2" power="1" id="7" class="zoom" style="position: absolute; margin: 0px; top: 20px; left: 0px; width: 1140px; height: 420px;"><iframe style="width: 940px; height: 420px;" marginheight="0" marginwidth="0" src="http://192.168.178.10/emoncms/vis/zoom?embed=1&amp;power=1&amp;kwhd=2&amp;currency=Eur&amp;pricekwh=0.21" scrolling="no" frameborder="0"></iframe></div>','height' => '440','name' => 'Verbruik','alias' => 'verbruik','description' => 'Energie verbruik','main' => '1','public' => '1','published' => '1','showdescription' => '1'),
  array('id' => '7','userid' => '1','content' => NULL,'height' => NULL,'name' => 'no name','alias' => '','description' => 'no description','main' => NULL,'public' => NULL,'published' => NULL,'showdescription' => NULL)
);

// `emoncms`.`feeds`
$feeds = array(
  array('id' => '1','name' => 'Verbruikt gemiddeld Watt per uur','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '38.2182','status' => '0','datatype' => '1','public' => '1','size' => '0','engine' => '0'),
  array('id' => '2','name' => 'Verbruikt kWh per dag','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '5.98004','status' => '0','datatype' => '2','public' => '1','size' => '0','engine' => '0'),
  array('id' => '3','name' => 'Verbruikt kWh per jaar','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '3413.76','status' => '0','datatype' => '1','public' => '1','size' => '0','engine' => '0'),
  array('id' => '4','name' => 'Geleverd gemiddeld Watt per uur','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '0','status' => '0','datatype' => '1','public' => '1','size' => '0','engine' => '0'),
  array('id' => '5','name' => 'Geleverd kWh per dag','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '0','status' => '0','datatype' => '2','public' => '1','size' => '0','engine' => '0'),
  array('id' => '6','name' => 'Geleverd kWh per jaar','userid' => '1','tag' => '','time' => '2013-03-26 20:41:18','value' => '0','status' => '0','datatype' => '1','public' => '1','size' => '0','engine' => '0')
);

// `emoncms`.`feed_1`
$feed_1 = array(
  array('time' => '1434758400','data' => '0')
);

// `emoncms`.`feed_3`
$feed_3 = array(
  array('time' => '2015','data' => '0')
);

// `emoncms`.`feed_4`
$feed_4 = array(
  array('time' => '1434758400','data' => '0')
);

// `emoncms`.`feed_6`
$feed_6 = array(
  array('time' => '2015','data' => '0')
);

// `emoncms`.`multigraph`
$multigraph = array(
  array('id' => '1','name' => '','userid' => '1','feedlist' => '[{"id":"1","name":"Elektriciteitsmeter verbruik","datatype":"1","timeWindow":2592000000,"end":0},{"id":"2","name":"Verbruik in Watt","datatype":"1"}]'),
  array('id' => '5','name' => NULL,'userid' => '1','feedlist' => '')
);

// `emoncms`.`myelectric`
$myelectric = array(
  array('userid' => '1','data' => '{"powerfeed":1,"dailyfeed":2,"dailytype":2}')
);

// `emoncms`.`rememberme`
$rememberme = array(
//  array('userid' => '1','token' => '8ea14f05158d82e931c9c4e7648bc3a55d499968','persistentToken' => 'e51554c6149989599130529086fa26a46c8334e7','expire' => '2015-06-08 16:45:07')
);

// `emoncms`.`users`
$users = array(
//  array('id' => '1','username' => 'MijnGebruikersNaam','email' => 'mijn.email@gmail.com','password' => 'f4ef4e1af08723200a260e12d97af177d0d5cea4544e3f4d377d9a64fa0ce02c','salt' => '636','apikey_write' => '7010d41ba88e410f5929b9a9a6c6c596','apikey_read' => 'e76b25bc25a099f24acd579d6dc5c299','lastlogin' => NULL,'uphits' => '0','dnhits' => '0','admin' => '1','lang' => 'nl_NL','timeoffset' => '0','settingsarray' => NULL,'gravatar' => '','name' => '','location' => '','timezone' => '0','language' => 'en_EN','bio' => '')
);
