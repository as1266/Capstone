-- MySQL dump 10.16  Distrib 10.1.44-MariaDB, for debian-linux-gnueabihf (armv7l)
--
-- Host: localhost    Database: srs
-- ------------------------------------------------------
-- Server version	10.1.44-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `ActiveUnlockCodes`
--

DROP TABLE IF EXISTS `ActiveUnlockCodes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ActiveUnlockCodes` (
  `UnlockCode` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ActiveUnlockCodes`
--

LOCK TABLES `ActiveUnlockCodes` WRITE;
/*!40000 ALTER TABLE `ActiveUnlockCodes` DISABLE KEYS */;
INSERT INTO `ActiveUnlockCodes` VALUES (2995),(2738),(3638),(3840),(2388),(2377),(2561),(2888),(3664),(2027),(3141);
/*!40000 ALTER TABLE `ActiveUnlockCodes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ArchiveOrdersStocked`
--

DROP TABLE IF EXISTS `ArchiveOrdersStocked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ArchiveOrdersStocked` (
  `StockedOrderID` int(11) DEFAULT NULL,
  `EmployeeID` int(11) DEFAULT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `UnlockCode` int(11) DEFAULT NULL,
  `LockID` int(11) DEFAULT NULL,
  `DateTimeStocked` datetime DEFAULT NULL,
  `DateTimeRetrieved` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ArchiveOrdersStocked`
--

LOCK TABLES `ArchiveOrdersStocked` WRITE;
/*!40000 ALTER TABLE `ArchiveOrdersStocked` DISABLE KEYS */;
/*!40000 ALTER TABLE `ArchiveOrdersStocked` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmployeeAccess`
--

DROP TABLE IF EXISTS `EmployeeAccess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EmployeeAccess` (
  `employee_id` int(11) DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeeAccess`
--

LOCK TABLES `EmployeeAccess` WRITE;
/*!40000 ALTER TABLE `EmployeeAccess` DISABLE KEYS */;
/*!40000 ALTER TABLE `EmployeeAccess` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EmployeePins`
--

DROP TABLE IF EXISTS `EmployeePins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EmployeePins` (
  `pin` int(11) DEFAULT NULL,
  `employee_name` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EmployeePins`
--

LOCK TABLES `EmployeePins` WRITE;
/*!40000 ALTER TABLE `EmployeePins` DISABLE KEYS */;
INSERT INTO `EmployeePins` VALUES (131415,'John Smith'),(212223,'Zach Waters'),(313233,'Jake Farms');
/*!40000 ALTER TABLE `EmployeePins` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Lockers`
--

DROP TABLE IF EXISTS `Lockers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Lockers` (
  `locker_id` int(11) DEFAULT NULL,
  `in_use_status` text,
  `locked_status` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Lockers`
--

LOCK TABLES `Lockers` WRITE;
/*!40000 ALTER TABLE `Lockers` DISABLE KEYS */;
INSERT INTO `Lockers` VALUES (1,'FALSE','CLOSED');
/*!40000 ALTER TABLE `Lockers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Orders`
--

DROP TABLE IF EXISTS `Orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Orders` (
  `OrderID` int(11) DEFAULT NULL,
  `CustomerName` varchar(255) DEFAULT NULL,
  `CustomerEmail` varchar(255) DEFAULT NULL,
  `CustomerPhoneNumber` bigint(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Orders`
--

LOCK TABLES `Orders` WRITE;
/*!40000 ALTER TABLE `Orders` DISABLE KEYS */;
INSERT INTO `Orders` VALUES (10001,'Sam Smorkle','untpokerfiends@gmail.com',4693965461),(10002,'Sam Smorkle','cooper.snyder2626@gmail.com',2145559009);
/*!40000 ALTER TABLE `Orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `OrdersStocked`
--

DROP TABLE IF EXISTS `OrdersStocked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `OrdersStocked` (
  `StockedOrderID` int(11) DEFAULT NULL,
  `EmployeeID` int(11) DEFAULT NULL,
  `OrderID` int(11) DEFAULT NULL,
  `UnlockCode` int(11) DEFAULT NULL,
  `LockID` int(11) DEFAULT NULL,
  `DateTimeStocked` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `OrdersStocked`
--

LOCK TABLES `OrdersStocked` WRITE;
/*!40000 ALTER TABLE `OrdersStocked` DISABLE KEYS */;
/*!40000 ALTER TABLE `OrdersStocked` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `WorkingLocker`
--

DROP TABLE IF EXISTS `WorkingLocker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `WorkingLocker` (
  `locker_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `WorkingLocker`
--

LOCK TABLES `WorkingLocker` WRITE;
/*!40000 ALTER TABLE `WorkingLocker` DISABLE KEYS */;
/*!40000 ALTER TABLE `WorkingLocker` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-09 17:49:03
