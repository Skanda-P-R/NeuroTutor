-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 11, 2025 at 01:46 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `neuro_tutor_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `badges`
--

CREATE TABLE `badges` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `icon_filename` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `badges`
--

INSERT INTO `badges` (`id`, `name`, `description`, `icon_filename`) VALUES
(1, 'Code Fixer I', 'Corrected 5 code submissions', 'code_fixer_1_icon.png'),
(2, 'Code Fixer II', 'Corrected 10 code submissions', 'code_fixer_2_icon.png'),
(3, 'Syntax Surgeon', 'Corrected 25 code submissions', 'syntax_surgeon.png'),
(4, 'First Login', 'Awarded for the first login', 'first_login_icon.png'),
(5, 'Coin Collector I', 'Awarded after collecting 5 coins', 'coin_collector_1_icon.png'),
(6, 'Coin Collector II', 'Awarded after collecting 10 coins', 'coin_collector_2_icon.png'),
(7, 'Coin Collector III', 'Awarded after collecting 25 coins', 'coin_collector_3_icon.png'),
(8, 'First Debug', 'Debugged your first question', 'debug_first_icon.png'),
(9, 'Debug Mastery I', 'Debugged 5 questions', 'debug_mastery_1_icon.png'),
(10, 'Debug Mastery II', 'Debugged 10 questions', 'debug_mastery_2_icon.png'),
(11, 'Bug Slayer', 'Debugged 25 questions', 'bug_slayer_icon.png');

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `question_id` int(11) NOT NULL,
  `concept` varchar(50) DEFAULT NULL,
  `difficulty_level` int(11) DEFAULT NULL,
  `question_text` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`question_id`, `concept`, `difficulty_level`, `question_text`) VALUES
(1, 'Arrays', 2, 'Find the Maximum Subarray (Kadane’s Algorithm): Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum.'),
(2, 'Arrays', 1, 'Remove Duplicates from Sorted Array: Given a sorted array, remove the duplicates in-place such that each element appears only once.'),
(3, 'Arrays', 1, 'Two Sum: Given an array of integers and a target sum, return indices of the two numbers such that they add up to the target.'),
(4, 'Arrays', 2, 'Merge Intervals: Given an array of intervals, merge all overlapping intervals.'),
(5, 'Arrays', 2, 'Product of Array Except Self: Return an array answer such that answer[i] is the product of all the elements of nums except nums[i].'),
(6, 'Strings', 1, 'Valid Anagram: Given two strings, determine if one is an anagram of the other.'),
(7, 'Strings', 2, 'Longest Substring Without Repeating Characters: Find the length of the longest substring without repeating characters.'),
(8, 'Strings', 2, 'Reverse Words in a String: Given a string, reverse the order of words.'),
(9, 'Strings', 1, 'String Compression: Compress the string using the counts of repeated characters (e.g., \"aabcccccaaa\" becomes \"a2b1c5a3\").'),
(10, 'Strings', 2, 'Group Anagrams: Group strings that are anagrams of each other.'),
(11, 'Recursion', 1, 'Factorial Calculation: Write a recursive function to calculate the factorial of a number.'),
(12, 'Recursion', 1, 'Fibonacci Number: Return the nth Fibonacci number using recursion.'),
(13, 'Recursion', 2, 'Power Set: Generate all subsets of a set using recursion.'),
(14, 'Recursion', 2, 'Permutations of a String: Print all permutations of a given string using recursion.'),
(15, 'Recursion', 3, 'N-Queens Problem: Place n queens on an n x n chessboard such that no two queens threaten each other.');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `questions_debugged` int(11) DEFAULT 0,
  `codes_corrected` int(11) DEFAULT 0,
  `coins` int(11) DEFAULT 0,
  `last_coin_award` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_attempts`
--

CREATE TABLE `user_attempts` (
  `user_id` int(11) DEFAULT NULL,
  `question_id` int(11) DEFAULT NULL,
  `code_submitted` text DEFAULT NULL,
  `understanding_score` float DEFAULT NULL,
  `attempt_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_badges`
--

CREATE TABLE `user_badges` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `badge_id` int(11) NOT NULL,
  `awarded_on` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user_retention`
--

CREATE TABLE `user_retention` (
  `user_id` int(11) NOT NULL,
  `concept` varchar(50) NOT NULL,
  `retention_score` float DEFAULT 0.5,
  `last_attempt` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `badges`
--
ALTER TABLE `badges`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`question_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `user_badges`
--
ALTER TABLE `user_badges`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`badge_id`),
  ADD KEY `badge_id` (`badge_id`);

--
-- Indexes for table `user_retention`
--
ALTER TABLE `user_retention`
  ADD PRIMARY KEY (`user_id`,`concept`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `badges`
--
ALTER TABLE `badges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_badges`
--
ALTER TABLE `user_badges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_badges`
--
ALTER TABLE `user_badges`
  ADD CONSTRAINT `user_badges_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_badges_ibfk_2` FOREIGN KEY (`badge_id`) REFERENCES `badges` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
