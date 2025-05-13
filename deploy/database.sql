CREATE
DATABASE IF NOT EXISTS temp_aisearch CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

CREATE TABLE IF NOT EXISTS `aisearch_conversation`
(
    `id`          INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `user_id`     INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '用户ID',
    `query`       VARCHAR(255) NOT NULL DEFAULT '' COMMENT '搜索查询内容',
    `mode`        VARCHAR(64)  NOT NULL DEFAULT 'simple' COMMENT '搜索模式',
    `deleted`     TINYINT UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除(0:正常;1:删除)',
    `create_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY           `idx_user_id` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='会话记录表';


CREATE TABLE IF NOT EXISTS `aisearch_conversation_message`
(
    `id`              INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `conversation_id` INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '会话ID',
    `query`           text     NOT NULL COMMENT '查询内容',
    `answer`          text     NOT NULL COMMENT 'AI回答问题',
    `deleted`         TINYINT  NOT NULL DEFAULT '0' COMMENT '删除(0:正常;1:删除)',
    `create_time`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY               `idx_conversation_id` (`conversation_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='消息记录表';


CREATE TABLE IF NOT EXISTS `aisearch_conversation_reference`
(
    `id`              INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `conversation_id` INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '会话ID',
    `message_id`      INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '消息ID',
    `crawl_id`        BIGINT UNSIGNED NOT NULL DEFAULT '0' COMMENT 'aisearch_crawl表的ID',
    `deleted`         TINYINT UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除(0:正常;1:删除)',
    `create_time`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time`     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    KEY               `idx_conversation_message_id` (`conversation_id`,`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='消息引用表';


CREATE TABLE IF NOT EXISTS `aisearch_crawl`
(
    `id`          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `doc_id`      VARCHAR(64)   NOT NULL DEFAULT '' COMMENT '网页文档的唯一ID',
    `hit_count`   INT UNSIGNED NOT NULL DEFAULT '0' COMMENT '命中次数',
    `title`       VARCHAR(4096) NOT NULL DEFAULT '' COMMENT '来源标题',
    `url`         VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '链接',
    `description` VARCHAR(4096) NOT NULL DEFAULT '' COMMENT '搜索引擎返回的内容描述',
    `icon`        VARCHAR(255)  NOT NULL DEFAULT '' COMMENT '图标',
    `source`      VARCHAR(64)   NOT NULL DEFAULT '' COMMENT '来源',
    `source_name` VARCHAR(128)  NOT NULL DEFAULT '' COMMENT '来源名称',
    `content`     MEDIUMTEXT    NOT NULL COMMENT '经过清洗处理后的网页内容',
    `deleted`     TINYINT UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除(0:正常;1:删除)',
    `create_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time` DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`),
    UNIQUE KEY `uk_doc_id` (`doc_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='网页内容表';


CREATE TABLE IF NOT EXISTS `aisearch_knowledge_movie`
(
    `id`            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'ID',
    `name`          VARCHAR(512)  NOT NULL DEFAULT '' COMMENT '电影名称',
    `category_json` VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '电影类型JSON格式',
    `duration`      VARCHAR(64)   NOT NULL DEFAULT '' COMMENT '电影时长',
    `country_json`  VARCHAR(1024) NOT NULL DEFAULT '' COMMENT '国家',
    `showtime`      VARCHAR(64)   NOT NULL DEFAULT '' COMMENT '上映时间',
    `description`   VARCHAR(4096) NOT NULL DEFAULT '' COMMENT '电影简介',
    `score`         DECIMAL(2, 1) NOT NULL DEFAULT 0.0 COMMENT '电影评分',
    `deleted`       TINYINT UNSIGNED NOT NULL DEFAULT '0' COMMENT '删除(0:正常;1:删除)',
    `create_time`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    `update_time`   DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='电影知识数据表';
