--
-- MySQL 5.5.38
-- Sun, 02 Jul 2017 06:29:59 +0000
--
-- つかいかた
-- 登録時はイベント名(event_name)、サークル名(circle_name)、スペース番号(space_no)、ペンネーム(pen_name)が必須です。
-- スペース番号は必ずX-YYz（X=島記号、YY=スペース番号、z=スペース補助番号aかbか）という形で登録してください。
-- プログラムからはevent_nameをlikeなりで引っ掛けて使ってください。

CREATE TABLE `toho_novels` (
   `id` int(7) not null auto_increment,
   `event_name` varchar(64) not null,
   `circle_name` varchar(64) not null,
   `space_no` varchar(10) not null,
   `pen_name` varchar(64) not null,
   `new_books` varchar(256),
   `new_book_values` varchar(256),
   `url` varchar(512),
   `web_catalog_url` varchar(512),
   `twitter` varchar(512),
   `tag` varchar(256),
   `shops` varchar(1024),
   PRIMARY KEY (`id`),
   KEY `event_name` (`event_name`),
   KEY `circle_name` (`circle_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1;