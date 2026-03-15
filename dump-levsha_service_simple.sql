-- MySQL dump 10.13  Distrib 8.4.7, for Win64 (x86_64)
--
-- Host: localhost    Database: levsha_service_simple
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `callback_requests`
--

DROP TABLE IF EXISTS `callback_requests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `callback_requests` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `processed_by` bigint unsigned DEFAULT NULL COMMENT 'Обработал менеджер (users.id)',
  PRIMARY KEY (`id`),
  KEY `processed_by` (`processed_by`),
  KEY `idx_callback_phone` (`phone`),
  KEY `idx_callback_status` (`status`),
  CONSTRAINT `callback_requests_ibfk_1` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `callback_requests`
--

LOCK TABLES `callback_requests` WRITE;
/*!40000 ALTER TABLE `callback_requests` DISABLE KEYS */;
INSERT INTO `callback_requests` VALUES (1,'+79990000002','new','2025-11-25 14:43:36',2),(2,'+79990000005','new','2025-11-25 14:43:37',3),(3,'+79990000001','new','2025-11-25 14:43:37',NULL);
/*!40000 ALTER TABLE `callback_requests` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `feedback_forms`
--

DROP TABLE IF EXISTS `feedback_forms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `feedback_forms` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `client_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subject` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `message` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `processed_by` bigint unsigned DEFAULT NULL COMMENT 'Кто обработал (users.id)',
  PRIMARY KEY (`id`),
  KEY `processed_by` (`processed_by`),
  CONSTRAINT `feedback_forms_ibfk_1` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `feedback_forms`
--

LOCK TABLES `feedback_forms` WRITE;
/*!40000 ALTER TABLE `feedback_forms` DISABLE KEYS */;
INSERT INTO `feedback_forms` VALUES (1,'Павел Смирнов','+79990000001','pavel.smirnov@mail.ru','Не работает динамик','Подскажите стоимость замены динамика на iPhone X.','done','2025-11-25 14:43:36',2),(2,'Анна Ким','+79990000004','anna.kim@mail.ru','Срок ремонта','Сколько по времени меняют стекло Samsung S20?','in_progress','2025-11-25 14:43:36',3),(3,'Максим Беляев','+79990000003','maxim.belyaev@mail.ru','Запись','Хочу записаться на диагностику в субботу.','new','2025-11-25 14:43:36',NULL);
/*!40000 ALTER TABLE `feedback_forms` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_number` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_id` bigint unsigned DEFAULT NULL COMMENT 'Клиент (users.id)',
  `client_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `client_phone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `device_model` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `problem_description` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `diagnostic_result` text COLLATE utf8mb4_unicode_ci,
  `status` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'new',
  `approx_price` decimal(10,2) DEFAULT NULL,
  `final_price` decimal(10,2) DEFAULT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `manager_id` bigint unsigned DEFAULT NULL COMMENT 'Сотрудник, оформивший заказ (users.id)',
  `master_id` bigint unsigned DEFAULT NULL COMMENT 'Мастер, выполняющий ремонт (users.id)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `client_id` (`client_id`),
  KEY `manager_id` (`manager_id`),
  KEY `master_id` (`master_id`),
  KEY `idx_orders_phone` (`client_phone`),
  KEY `idx_orders_status` (`status`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`manager_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT,
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`master_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (1,'L-0001',6,'Смирнов Павел Ильич','+79990000001','iPhone X','Не работает разговорный динамик','Динамик пробит, требуется замена','ready',2500.00,2800.00,'2025-11-25 14:43:37',NULL,2,4),(2,'L-0002',7,'Исаева Татьяна Петровна','+79990000002','Samsung Galaxy S20','Треснуло стекло экрана','Требуется замена дисплейного модуля','in_work',7000.00,NULL,'2025-11-25 14:43:37',NULL,3,5),(3,'L-0003',8,'Беляев Максим Сергеевич','+79990000003','Xiaomi Redmi Note 10','Телефон не включается','Проблема в контроллере питания','diagnostics',1500.00,NULL,'2025-11-25 14:43:37',NULL,2,4),(4,'L-0004',9,'Ким Анна Владимировна','+79990000004','iPhone 12','Быстро разряжается','Батарея изношена на 82%','ready',3000.00,3500.00,'2025-11-25 14:43:37',NULL,3,5),(5,'L-0005',10,'Морозов Денис Андреевич','+79990000005','Huawei P30','Не работает камера','Неисправность модуля основной камеры','new',2000.00,NULL,'2025-11-25 14:43:37',NULL,2,NULL);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `order_id` bigint unsigned DEFAULT NULL,
  `client_id` bigint unsigned DEFAULT NULL COMMENT 'Клиент (users.id)',
  `rating` tinyint unsigned NOT NULL COMMENT 'Оценка 1–5',
  `comment` text COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `is_published` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `client_id` (`client_id`),
  KEY `idx_reviews_rating` (`rating`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`client_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE RESTRICT
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,1,6,5,'Отличный сервис! Быстро поменяли динамик, телефон работает как новый.','2025-11-25 14:43:37',1),(2,4,9,4,'Поменяли батарею быстро, но хотелось бы дешевле.','2025-11-25 14:43:37',1),(3,2,7,3,'Жду, когда приедут запчасти. Надеюсь, починят хорошо.','2025-11-25 14:43:37',0),(4,NULL,8,5,'Всегда чиню технику у вас, лучший сервис в городе!','2025-11-25 14:43:37',1);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Логин (для клиентов может быть NULL)',
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT 'Хэш пароля (для клиентов может быть NULL)',
  `full_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT 'ФИО клиента или сотрудника',
  `role` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'client' COMMENT 'client, manager, master, admin',
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `email` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin1','hash_admin','Иванов Сергей Петрович','admin','+79000000001','admin@levsha.ru',1,'2025-11-25 14:43:36'),(2,'manager1','admin123','Петрова Мария Андреевна','manager','+79000000002','petrova@levsha.ru',1,'2025-11-25 14:43:36'),(3,'manager2','hash_mgr2','Горбунов Алексей Юрьевич','manager','+79000000003','gorbunov@levsha.ru',1,'2025-11-25 14:43:36'),(4,'master1','admin123','Кузнецов Дмитрий Олегович','master','+79000000004','kuznetsov@levsha.ru',1,'2025-11-25 14:43:36'),(5,'master2','hash_mst2','Серебряков Артём Николаевич','master','+79000000005','serebryakov@levsha.ru',1,'2025-11-25 14:43:36'),(6,NULL,NULL,'Смирнов Павел Ильич','client','+79990000001','pavel.smirnov@mail.ru',1,'2025-11-25 14:43:36'),(7,NULL,NULL,'Исаева Татьяна Петровна','client','+79990000002','tatiana.isaeva@mail.ru',1,'2025-11-25 14:43:36'),(8,NULL,NULL,'Беляев Максим Сергеевич','client','+79990000003','maxim.belyaev@mail.ru',1,'2025-11-25 14:43:36'),(9,NULL,NULL,'Ким Анна Владимировна','client','+79990000004','anna.kim@mail.ru',1,'2025-11-25 14:43:36'),(10,NULL,NULL,'Морозов Денис Андреевич','client','+79990000005','denis.morozov@mail.ru',1,'2025-11-25 14:43:36'),(11,'admin','admin123','Админ','admin','89998887766','admin@admin.ru',1,'2025-11-25 15:54:09');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'levsha_service_simple'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-27 23:50:08
