  -- ServerPython MySQL  --

CREATE DATABASE library;
use library;

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user` varchar(256) NULL,
  `password` varchar(40) NULL,
  `email` varchar(256) NOT NULL,
  `guser` tinyint(1) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE(user, email)
);

CREATE TABLE `genres` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `genre` varchar(15) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE(genre)
);

CREATE TABLE `author` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `first` varchar(20) NOT NULL,
  `last` varchar(20) NOT NULL,
  `biography` text NULL,
  `photo` varchar(10) NULL,
  PRIMARY KEY (id)
);

CREATE TABLE `collections`(
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `namecollection` varchar(40) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE(namecollection)
);

CREATE TABLE `books` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `idgenre` bigint(20) NOT NULL,
  `idauthor` bigint(20) NOT NULL,
  `idcollect` bigint(20) NULL,
  `photo` varchar(10) NULL,
  `tlines` bigint(20) NOT NULL,
  `bfile` varchar(10) NOT NULL,
  `bname` varchar(50) NOT NULL,
  `synopsis` text NOT NULL,
   PRIMARY KEY (id),
   UNIQUE(bfile, bname),
   FOREIGN KEY (idgenre) REFERENCES genres(id),
   FOREIGN KEY (idauthor) REFERENCES author(id),
   FOREIGN KEY (idcollect) REFERENCES collections(id)
);

CREATE TABLE `readings` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iduser` bigint(20) NOT NULL,
  `idbook` bigint(20) NOT NULL,
  `alines` bigint(20) NOT NULL,
  `lastreading` datetime NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (iduser) REFERENCES users(id),
  FOREIGN KEY (idbook) REFERENCES books(id),
  UNIQUE KEY `ids_readings` (iduser, idbook)
);

CREATE TABLE `read_later`(
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `iduser` bigint(20) NOT NULL,
  `idbook` bigint(20) NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (iduser) REFERENCES users(id),
  FOREIGN KEY (idbook) REFERENCES books(id),
  UNIQUE KEY `ids_read_later` (iduser, idbook)
);

INSERT INTO `users`(`id`, `user`, `password`, `email`, `guser`) VALUES
  (NULL, NULL, '265392dc2782778664cc9d56c8e3cd9956661bb0', 'U2FsdGVkX1+PFfvEXxBYU/Uu7eo0kEzUepmMdVv7GOA=', '0');

INSERT INTO `author`(`id`, `first`, `last`, `biography`, `photo`) VALUES
  (NULL, 'J. R. R.', 'Tolkien', 'John Ronald Reuel Tolkien was an English writer, poet, philologist, and university professor who is best known as the author of the classic high fantasy works The Hobbit, The Lord of the Rings, and The Silmarillion.', 'tolkien'),
  (NULL, 'George R. R.', 'Martin', 'George Raymond Richard Martin is an American novelist and short-story writer in the fantasy, horror, and science fiction genres, screenwriter, and television producer. He is best known for his series of epic fantasy novels, A Song of Ice and Fire, which was later adapted into the HBO series Game of Thrones (2011–present).', 'grrm'),
  (NULL, 'Stephen', 'King', 'Stephen Edwin King is an American author of horror, supernatural fiction, suspense, science fiction, and fantasy. His books have sold more than 350 million copies, many of which have been adapted into feature films, miniseries, television series, and comic books. King has published 54 novels, including seven under the pen name Richard Bachman, and six non-fiction books. He has written around 200 short stories, most of which have been collected in book collections.', 'stephking'),
  (NULL, 'J. K.', 'Rowling', 'Joanne Rowling, (born 31 July 1965), writing under the pen names J. K. Rowling and Robert Galbraith, is a British novelist, philanthropist, film producer, television producer and screenwriter best known for writing the Harry Potter fantasy series. The books have won multiple awards, and sold more than 400 million copies, becoming the best-selling book series in history. They have also been the basis for a film series, over which Rowling had overall approval on the scripts and was a producer on the final films in the series.', 'jkrowling'),
  (NULL, 'Lorem Ipsum', 'The Author', 'In publishing and graphic design, lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document without relying on meaningful content (also called greeking). Replacing the actual content with placeholder text allows designers to design the form of the content before the content itself has been produced.', 'lorem');

INSERT INTO `genres`(`genre`) VALUES
  ('fantasy'),
  ('drama'),
  ('action'),
  ('horror');

INSERT INTO `collections` (`id`, `namecollection`) VALUES
  (NULL, 'The Lord of the Rings'),
  (NULL, 'A Song of Ice and Fire'),
  (NULL, 'Harry Potter');

INSERT INTO `books`(`id`, `idgenre`, `idauthor`, `idcollect`, `photo`, `tlines`, `bfile`, `bname`, `synopsis`) VALUES
  (NULL, '1', '1', '1', 'lotr1', '14967', 'lotr1', 'The Fellowship of the Ring', 'The Fellowship of the Ring is the first of three volumes in The Lord of the Rings, an epic set in the fictional world of Middle-earth. The Lord of the Rings is an entity named Sauron, the Dark Lord, who long ago lost the One Ring that contains much of his power. His overriding desire is to reclaim the Ring and use it to enslave all of Middle-earth.'),
  (NULL, '1', '1', '1', 'lotr2', '12424', 'lotr2', 'The Two Towers', 'The Two Towers opens with the disintegration of the Fellowship, as Merry and Pippin are taken captive by Orcs after the death of Boromir in battle. The Orcs, having heard a prophecy that a Hobbit will bear a Ring that gives universal power to its owner, wrongly think that Merry and Pippin are the Ring-bearers.'),
  (NULL, '1', '1', '1', 'lotr3', '12716', 'lotr3', 'The Return of the King', 'The Return of the King, the third and final volume in The Lord of the Rings, opens as Gandalf and Pippin ride east to the city of Minas Tirith in Gondor, just after parting with King Théoden and the Riders of Rohan at the end of The Two Towers. In Minas Tirith, Gandalf and Pippin meet Denethor, the city’s Steward, or ruler, who clearly dislikes Gandalf. Pippin offers Denethor his sword in service to Gondor, out of gratitude for the fact that Denethor’s son Boromir gave his life for the hobbits earlier in the quest.'),
  (NULL, '3', '2', '2', 'gt1', '23934', 'gt1', 'A Game of Thrones', 'At the beginning of the story, Lord Eddard "Ned" Stark executes a deserter from the Night''s Watch, who has betrayed his vows and fled from the Wall. On the way back, his children adopt six direwolf pups, the animal of his sigil. There are three male and two female direwolf pups, as well as an albino runt, which aligns with his three trueborn sons, two trueborn daughters, and one bastard son. That night, Ned receives word of the death of his mentor, Lord Jon Arryn, the principal advisor to Ned''s childhood friend, King Robert Baratheon. During his own visit to Ned''s castle of Winterfell, Robert recruits Ned to replace Arryn as the King''s Hand. Ned is reluctant, but agrees to go when he learns that Arryn''s widow Lysa believes Queen Cersei Lannister and her family poisoned Arryn. Shortly thereafter, Ned''s son Bran inadvertently discovers Cersei having sex with her twin brother Jaime Lannister, who throws Bran from the tower to conceal their affair.'),
  (NULL, '3', '2', '2', 'gt2', '23307', 'gt2', 'A Clash of Kings', 'With King Robert Baratheon dead, his alleged son Joffrey and brothers Renly and Stannis all claim the throne of Westeros. Robb Stark is declared ''King in the North'' while Balon Greyjoy declares himself king of the Iron Islands and attacks the western coast of the North. Robb''s younger brother Bran Stark finds new friends in Jojen and Meera Reed.'),
  (NULL, '2', '3', '3', 'hp1', '8431', 'hp1', 'Harry Potter and the Philosopher''s Stone', 'Harry Potter has been living an ordinary life, constantly abused by his surly and cold aunt and uncle, Vernon and Petunia Dursley and bullied by their spoiled son Dudley since the death of his parents ten years prior. His life changes on the day of his eleventh birthday when he receives a letter of acceptance into a Hogwarts School of Witchcraft and Wizardry, delivered by a half-giant named Rubeus Hagrid after previous letters had been destroyed by Vernon and Petunia. Hagrid explains Harry''s hidden past as the wizard son of James and Lily Potter, who were a wizard and witch respectively, and how they were murdered by the most evil and powerful dark wizard of all time, Lord Voldemort, which resulted in the one-year-old Harry being sent to live with his aunt and uncle. The strangest bit of the murder was how Voldemort was unable to kill him, but instead had his own powers removed and blasted away, sparking Harry''s immense fame among the magical community.'),
  (NULL, '2', '3', '3', 'hp2', '10355', 'hp2', 'Harry Potter and the Chamber of Secrets', 'On Harry Potter''s birthday in 1992, the Dursley family—Harry''s Uncle Vernon, Aunt Petunia, and cousin Dudley—hold a dinner party for a potential client of Vernon''s drill-manufacturing company. Harry is not invited, but is content to spend the evening quietly in his bedroom, although he is confused that his school friends have not sent cards or presents. However, when he goes to his room, a house-elf named Dobby warns him not to return to Hogwarts and admits to intercepting Harry''s post from his friends. Having failed to persuade Harry to voluntarily give up his place at Hogwarts, Dobby then attempts to get him expelled by using magic to smash Petunia''s dessert on a dinner party guest and framing it on Harry, who is not allowed to use magic out of school. Uncle Vernon''s business deal falls through, but Harry is given a second chance from the Ministry of Magic, and allowed to return at the start of the school year.'),
  (NULL, '1', '3', NULL, 'greenmile', '8236', 'greenmile', 'The Green Mile', 'A first-person narrative told by Paul Edgecombe, the novel switches between Paul as an old man in the Georgia Pines nursing home sharing his story with fellow resident Elaine Connelly in 1996, and his time in 1932 as the block supervisor of the Cold Mountain Penitentiary death row, nicknamed "The Green Mile" for the color of the floor''s linoleum'),
  (NULL, '4', '3', NULL, 'shining', '15347', 'shining', 'The Shining', 'The Shining mainly takes place in the fictional Overlook Hotel, an isolated, haunted resort located in the Colorado Rockies. The history of the hotel, which is described in backstory by several characters, includes the deaths of some of its guests and of former winter caretaker Delbert Grady, who succumbed to cabin fever and killed his family and himself.'),
  (NULL, '4', '3', NULL, 'it', '39489', 'it', 'It', 'During a heavy rainstorm in Derry, Maine, six-year-old George "Georgie" Denbrough is chasing a paper boat that was given to him by his older brother, Bill, down a gutter. The boat is washed down a storm drain and Georgie peers in, seeing a pair of glowing yellow eyes. Georgie is confronted by a man dressed in a silver clown suit who introduces himself as "Mr. Bob Gray", a.k.a. "Pennywise the Dancing Clown". Pennywise offers Georgie a balloon which he cautiously refuses. The clown then entices Georgie to reach into the drain to retrieve his boat and severs his arm, causing his death.'),
  (NULL, '2', '5', NULL, 'lorem', '101', 'lorem', 'Lorem Drama', 'Lorem Drama is simply dummy text of the printing and typesetting industry. Lorem Drama has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Drama.'),
  (NULL, '1', '5', NULL, 'lorem', '101', 'lorem', 'Lorem Fantasy', 'Lorem Fantasy is simply dummy text of the printing and typesetting industry. Lorem Fantasy has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Fantasy.'),
  (NULL, '4', '5', NULL, 'lorem', '101', 'lorem', 'Lorem Horror', 'Lorem Horror is simply dummy text of the printing and typesetting industry. Lorem Horror has been the industry''s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Horror.');
  
  -- ServerApp SQLite  --
  
CREATE TABLE IF NOT EXISTS `users` (
    `id` INTEGER PRIMARY KEY,
    `user` varchar(256) NULL,
    `pass` varchar(40) NULL,
    `email` varchar(256) NOT NULL,
    `guser` tinyint(1) NOT NULL, 
    `token` varchar(256) NOT NULL
    );