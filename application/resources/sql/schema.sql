SET NAMES utf8mb4;
SET
    FOREIGN_KEY_CHECKS = 0;

CREATE
    DATABASE IF NOT EXISTS iotdb;
use
    iotdb;

DROP TABLE IF EXISTS `userinfo`;
create TABLE `userinfo`
(
    `id`          int(11)      auto_increment                                                 NOT NULL AUTO_INCREMENT,
    `pictureurl` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    `ismasked`       int(11) NOT NULL,
    `gender` int(11) NOT NULL,
    `timeNow`       varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
    PRIMARY KEY (`id`) USING BTREE
) COMMENT = 'pictures'
    ENGINE = InnoDB
    AUTO_INCREMENT = 1
    CHARACTER SET = utf8mb4
    COLLATE = utf8mb4_general_ci
    ROW_FORMAT = Dynamic;