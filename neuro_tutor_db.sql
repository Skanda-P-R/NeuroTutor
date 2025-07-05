-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 05, 2025 at 04:02 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

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
(11, 'Bug Slayer', 'Debugged 25 questions', 'bug_slayer_icon.png'),
(12, 'Array Builder', 'Awarded for achieving 0.6 retention in Arrays.', 'array_builder.png'),
(13, 'Array Master', 'Awarded for achieving 0.8 retention in Arrays.', 'array_master.png'),
(14, 'String Builder', 'Awarded for achieving 0.6 retention in Strings.', 'string_builder.png'),
(15, 'String Master', 'Awarded for achieving 0.8 retention in Strings.', 'string_master.png'),
(16, 'Recursion Builder', 'Awarded for achieving 0.6 retention in Recursion.', 'recursion_builder.png'),
(17, 'Recursion Master', 'Awarded for achieving 0.8 retention in Recursion.', 'recursion_master.png');

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
(15, 'Recursion', 3, 'N-Queens Problem: Place n queens on an n x n chessboard such that no two queens threaten each other.'),
(16, 'Linked Lists', 1, 'Reverse a Linked List: Reverse a singly linked list.'),
(17, 'Linked Lists', 2, 'Detect Cycle in Linked List: Check if a linked list contains a cycle.'),
(18, 'Linked Lists', 2, 'Merge Two Sorted Lists: Merge two sorted linked lists into one.'),
(19, 'Linked Lists', 3, 'Intersection of Two Linked Lists: Find the node at which two linked lists intersect.'),
(20, 'Linked Lists', 3, 'Copy List with Random Pointer: Create a deep copy of a linked list with random pointers.'),
(21, 'Trees', 1, 'Maximum Depth of Binary Tree: Find the maximum depth of a binary tree.'),
(22, 'Trees', 1, 'Validate Binary Search Tree: Check if a binary tree is a valid BST.'),
(23, 'Trees', 2, 'Symmetric Tree: Check if a tree is symmetric around its center.'),
(24, 'Trees', 2, 'Binary Tree Level Order Traversal: Return the level order traversal of a binary tree.'),
(25, 'Trees', 3, 'Serialize and Deserialize Binary Tree: Design algorithms to serialize and deserialize a binary tree.'),
(26, 'Graphs', 1, 'Number of Islands: Count the number of islands in a grid (DFS/BFS).'),
(27, 'Graphs', 2, 'Clone Graph: Return a deep copy of a graph.'),
(28, 'Graphs', 2, 'Course Schedule: Determine if it\'s possible to finish all courses given prerequisites.'),
(29, 'Graphs', 3, 'Word Ladder: Find the shortest transformation sequence from beginWord to endWord.'),
(30, 'Graphs', 3, 'Pacific Atlantic Water Flow: Find cells where water can flow to both the Pacific and Atlantic ocean.'),
(31, 'Dynamic Programming', 1, 'Climbing Stairs: Count distinct ways to climb stairs with 1 or 2 steps.'),
(32, 'Dynamic Programming', 2, 'House Robber: Max sum of non-adjacent elements (house robbery problem).'),
(33, 'Dynamic Programming', 2, 'Coin Change: Find minimum coins to make a given amount.'),
(34, 'Dynamic Programming', 3, 'Longest Increasing Subsequence: Find the length of the longest increasing subsequence.'),
(35, 'Dynamic Programming', 3, 'Edit Distance: Find the minimum number of operations to convert one string to another.'),
(36, 'Sorting & Searching', 1, 'Binary Search: Implement binary search on a sorted array.'),
(37, 'Sorting & Searching', 2, 'Search in Rotated Sorted Array: Find a target in a rotated sorted array.'),
(38, 'Sorting & Searching', 2, 'Kth Largest Element in an Array: Find the kth largest element using sorting or heap.'),
(39, 'Sorting & Searching', 3, 'Merge Sort: Implement merge sort algorithm.'),
(40, 'Sorting & Searching', 3, 'Quick Sort: Implement quick sort algorithm.');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `question_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=41;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user_badges`
--
ALTER TABLE `user_badges`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=39;

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
