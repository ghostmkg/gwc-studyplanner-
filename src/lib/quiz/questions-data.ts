import type { QuizCategory } from './types';

// Corrected some answers and minor details.
// Note: The user provided "questions" as the const name. I'm using "سوالات" (Persian for questions)
// as per the original file to avoid breaking existing imports if they are sensitive to this.
// For clarity in English, it would typically be "quizCategoriesData" or similar.

export const سوالات: QuizCategory[] = [
  {
    category: "Programming",
    slug: "programming",
    icon: "Laptop", // Example Lucide icon name
    description: "Test your knowledge of programming languages and concepts.",
    questions: [
      {
        question: "What does HTML stand for?",
        options: ["Hyper Text Pre Processor", "Hyper Text Markup Language", "Hyper Text Multiple Language", "Hyper Tool Multi Language"],
        correctAnswer: 1,
      },
      {
        question: "Which of the following is a correct way to declare a variable in JavaScript?",
        options: ["var x = 10;", "variable x = 10;", "int x = 10;", "let 10 = x;"],
        correctAnswer: 0,
      },
      {
        question: "How do you write a single-line comment in Python?",
        options: ["// This is a comment", "# This is a comment", "/* This is a comment */", "<!-- This is a comment -->"],
        correctAnswer: 1, // Corrected from potentially wrong index
      },
      {
        question: "What does CSS stand for?",
        options: ["Cascading Style Sheets", "Colorful Style Sheets", "Computer Style Sheets", "Cascading Simple Sheets"],
        correctAnswer: 0,
      },
      {
        question: "In JavaScript, how do you create a function?",
        options: ["create function myFunction()", "def function myFunction()", "func myFunction()", "function myFunction()"],
        correctAnswer: 3,
      },
      {
        question: "What does the 'typeof' operator do in JavaScript?",
        options: ["Checks the type of a variable", "Declares a variable", "Assigns a value to a variable", "Converts a variable to another type"],
        correctAnswer: 0,
      },
      {
        question: "In C, how do you typically define a function that does not return a value?",
        options: ["function myFunction()", "def myFunction()", "void myFunction()", "func myFunction()"],
        correctAnswer: 2,
      },
      {
        question: "Which of the following is a characteristic of Python?",
        options: ["Statically typed", "Compiled language", "Low-level language", "Dynamically typed"],
        correctAnswer: 3, // Corrected
      },
      {
        question: "Which language is commonly used for Android app development?",
        options: ["Swift", "Java", "C#", "Python"],
        correctAnswer: 1, // Java and Kotlin are common, Java is an option
      },
      {
        question: "What is the purpose of the 'forEach()' method in JavaScript for arrays?",
        options: ["Removes duplicate elements from an array", "Filters elements in an array based on a condition", "Sorts an array in place", "Executes a provided function once for each array element"],
        correctAnswer: 3,
      },
      {
        question: "What does the 'return' keyword do in a function?",
        options: ["Ends the function execution and optionally specifies a value to be returned to the caller", "Continues to the next iteration of a loop", "Exits the entire program", "Prints a value to the console"],
        correctAnswer: 0,
      },
      {
        question: "Which of the following is NOT a semantic HTML5 element?",
        options: ["<header>", "<footer>", "<span class='container'>", "<article>"],
        correctAnswer: 2, // `<span>` is generic, not semantic by itself
      },
      {
        question: "What is the primary purpose of a 'for' loop in programming?",
        options: ["To execute a block of code repeatedly for a known number of iterations", "To make a decision based on a condition", "To define a reusable block of code", "To handle errors and exceptions"],
        correctAnswer: 0,
      },
      {
        question: "Which data structure typically follows the LIFO (Last In, First Out) principle?",
        options: ["Queue", "Stack", "Linked List", "Tree"],
        correctAnswer: 1,
      },
      {
        question: "Which command is used in Git to save your staged changes to the local repository?",
        options: ["git commit -m 'message'", "git push", "git pull", "git stage ."],
        correctAnswer: 0,
      },
      {
        question: "What does the 'map()' function typically do in functional programming with arrays (e.g., in JavaScript)?",
        options: ["Sorts the array in place", "Filters out elements that don't meet a condition", "Creates a new array populated with the results of calling a provided function on every element in the calling array", "Modifies the original array by applying a function to each element"],
        correctAnswer: 2,
      },
      {
        question: "What does IDE stand for?",
        options: ["Integrated Development Environment", "Internal Drive Error", "Input Device Emulator", "Instruction Decode Engine"],
        correctAnswer: 0,
      },
      {
        question: "Which of the following is a key principle of object-oriented programming (OOP)?",
        options: ["Encapsulation", "Global variables", "Procedural execution", "Direct memory manipulation"],
        correctAnswer: 0,
      },
      {
        question: "What does SQL stand for?",
        options: ["Simple Question Language", "Systematic Query Language", "Standard Question Language", "Structured Query Language"],
        correctAnswer: 3,
      },
      {
        question: "Which of these is an example of a NoSQL (non-relational) database?",
        options: ["MongoDB", "MySQL", "PostgreSQL", "Oracle Database"],
        correctAnswer: 0,
      },
      {
        question: "How do you write a multi-line comment in CSS?",
        options: ["// This is a comment", "/* This is a comment */", "# This is a comment", "<!-- This is a comment -->"],
        correctAnswer: 1,
      },
      {
        question: "Which sorting algorithm repeatedly steps through the list, compares adjacent elements and swaps them if they are in the wrong order?",
        options: ["Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort"],
        correctAnswer: 0,
      },
      {
        question: "In Java, what is the primary purpose of the 'finally' block in a try-catch-finally statement?",
        options: ["To catch all types of exceptions", "To execute code only if an exception occurs", "To execute code regardless of whether an exception occurred or not, typically for cleanup", "To define the main execution path of the program"],
        correctAnswer: 2,
      },
      {
        question: "For very fast lookups (average O(1) time complexity), which data structure is often preferred if key-value pairs are needed?",
        options: ["Hash Table (or Dictionary/Map)", "Sorted Array", "Linked List", "Binary Search Tree"],
        correctAnswer: 0,
      },
      {
        question: "What is the correct basic syntax for an 'if' statement in JavaScript?",
        options: ["if (condition) { /* code */ }", "if condition then { /* code */ }", "if { /* code */ } where condition", "test (condition) then { /* code */ }"],
        correctAnswer: 0,
      },
    ],
  },
  {
    category: "Geography",
    slug: "geography",
    icon: "Globe",
    description: "Explore your knowledge about the world, its countries, and natural wonders.",
    questions: [
        {
          question: "Which is the longest river in the world?",
          options: ["Amazon River", "Nile River", "Yangtze River", "Mississippi River"],
          correctAnswer: 1,
        },
        {
          question: "Which country is known as the Land of the Rising Sun?",
          options: ["China", "South Korea", "Japan", "Thailand"],
          correctAnswer: 2,
        },
        {
          question: "What is the largest ocean in the world by surface area?",
          options: ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean", "Pacific Ocean"],
          correctAnswer: 3,
        },
        {
          question: "As of recent estimates, which country has the largest population in the world?",
          options: ["India", "China", "United States", "Indonesia"],
          correctAnswer: 0, // India surpassed China
        },
        {
          question: "Which country is home to the Great Barrier Reef, the world's largest coral reef system?",
          options: ["Australia", "Brazil", "South Africa", "Philippines"],
          correctAnswer: 0,
        },
        {
          question: "Which is the smallest independent state (country) in the world by area?",
          options: ["Monaco", "Nauru", "Vatican City", "San Marino"],
          correctAnswer: 2,
        },
        {
          question: "What is the tallest mountain in the world above sea level?",
          options: ["K2 (Mount Godwin-Austen)", "Kangchenjunga", "Mount Everest", "Lhotse"],
          correctAnswer: 2,
        },
        {
          question: "What is the capital city of Canada?",
          options: ["Ottawa", "Toronto", "Vancouver", "Montreal"],
          correctAnswer: 0,
        },
        {
          question: "Which desert is the largest hot desert in the world?",
          options: ["Gobi Desert", "Kalahari Desert", "Sahara Desert", "Arabian Desert"],
          correctAnswer: 2,
        },
        {
          question: "Which Scandinavian country is often called the 'Land of the Midnight Sun' due to its northern regions experiencing continuous daylight in summer?",
          options: ["Sweden", "Denmark", "Norway", "Finland"],
          correctAnswer: 2, // Also Finland and Sweden parts, but Norway is strongly associated.
        },
        {
          question: "What is the longest continental mountain range in the world?",
          options: ["Himalayas", "Rocky Mountains", "Andes", "Great Dividing Range"],
          correctAnswer: 2,
        },
        {
          question: "The ancient city of Thebes and the Valley of the Kings are located along which major river?",
          options: ["Tigris River", "Euphrates River", "Nile River", "Jordan River"],
          correctAnswer: 2,
        },
        {
          question: "What is the largest island in the world by land area?",
          options: ["Greenland", "New Guinea", "Borneo", "Madagascar"],
          correctAnswer: 0,
        },
        {
          question: "What is the capital city of Japan?",
          options: ["Kyoto", "Osaka", "Tokyo", "Sapporo"],
          correctAnswer: 2,
        },
        {
          question: "Which country spans the most time zones?",
          options: ["United States", "Russia", "Canada", "France (including overseas territories)"],
          correctAnswer: 3, // France due to its overseas territories. Russia if only contiguous.
        },
        {
          question: "The Eiffel Tower, a famous global landmark, is located in which European capital city?",
          options: ["Berlin", "Rome", "Madrid", "Paris"],
          correctAnswer: 3,
        },
        {
          question: "Which city is often cited as the most populous metropolitan area in the world?",
          options: ["Tokyo", "Delhi", "Shanghai", "São Paulo"],
          correctAnswer: 0,
        },
        {
          question: "The Andes mountain range is primarily located on which continent?",
          options: ["North America", "Africa", "Asia", "South America"],
          correctAnswer: 3,
        },
        {
          question: "Which continent is sometimes referred to as the 'Cradle of Humankind'?",
          options: ["Asia", "Africa", "Europe", "South America"],
          correctAnswer: 1,
        },
        {
          question: "What is the capital city of Brazil?",
          options: ["Rio de Janeiro", "São Paulo", "Brasília", "Salvador"],
          correctAnswer: 2,
        },
        {
          question: "What is the official language of Brazil?",
          options: ["Spanish", "English", "Portuguese", "French"],
          correctAnswer: 2,
        },
        {
          question: "Which country has the highest number of active volcanoes?",
          options: ["Japan", "Indonesia", "United States", "Chile"],
          correctAnswer: 1,
        },
        {
          question: "Which U.S. city is famously nicknamed the 'Big Apple'?",
          options: ["Los Angeles", "New York City", "Chicago", "Boston"],
          correctAnswer: 1,
        },
        {
          question: "The Indian Ocean is located to the east of which continent?",
          options: ["Australia", "South America", "Europe", "Africa"],
          correctAnswer: 3,
        },
        {
          question: "Which continent is the second largest by land area?",
          options: ["Asia", "Africa", "North America", "South America"],
          correctAnswer: 1,
        },
      ],
  },
  {
    category: "Mathematics",
    slug: "mathematics",
    icon: "Calculator",
    description: "Challenge your mathematical skills with these problems.",
    questions: [
        {
          question: "What is the square root of 144?",
          options: ["10", "11", "12", "13"],
          correctAnswer: 2,
        },
        {
          question: "What is 15 × 13?",
          options: ["180", "185", "195", "200"],
          correctAnswer: 2,
        },
        {
          question: "What is the value of 8³ (8 to the power of 3)?",
          options: ["512", "216", "256", "64"],
          correctAnswer: 0,
        },
        {
          question: "What is 48 ÷ 6?",
          options: ["7", "8", "9", "6"],
          correctAnswer: 1,
        },
        {
          question: "What is the value of 3 + 5 × 4 (following order of operations)?",
          options: ["32", "22", "24", "23"],
          correctAnswer: 3, // 5*4 = 20, 3+20 = 23
        },
        {
          question: "What is the sum of the interior angles in any triangle?",
          options: ["180°", "360°", "90°", "270°"],
          correctAnswer: 0,
        },
        {
          question: "What is the perimeter of a square with a side length of 4 cm?",
          options: ["12 cm", "16 cm", "20 cm", "8 cm"],
          correctAnswer: 1,
        },
        {
          question: "What is 11² (11 squared)?",
          options: ["100", "131", "141", "121"],
          correctAnswer: 3, // Corrected
        },
        {
          question: "What is 9 × 12?",
          options: ["105", "110", "108", "96"],
          correctAnswer: 2,
        },
        {
          question: "What is the value of 16 ÷ 4?",
          options: ["2", "3", "4", "8"],
          correctAnswer: 2,
        },
        {
          question: "What is 25% of 200?",
          options: ["25", "40", "50", "75"],
          correctAnswer: 2,
        },
        {
          question: "What is the area of a rectangle with length 5 cm and width 8 cm?",
          options: ["40 cm²", "13 cm²", "26 cm²", "30 cm²"],
          correctAnswer: 0,
        },
        {
          question: "What is the value of 10 ÷ 2 + 3 (following order of operations)?",
          options: ["8", "2.5", "5", "2"],
          correctAnswer: 0, // 10/2=5, 5+3=8. Original had 1, which is 7.
        },
        {
          question: "What is 3 × 7 + 2 (following order of operations)?",
          options: ["27", "23", "21", "13"],
          correctAnswer: 1, // 3*7=21, 21+2=23. Original had 1, which is 21. This means (3*7)+2.
        },
        {
          question: "What is the greatest common divisor (GCD) of 24 and 36?",
          options: ["4", "6", "8", "12"],
          correctAnswer: 3,
        },
        {
          question: "What is the least common multiple (LCM) of 6 and 8?",
          options: ["24", "12", "48", "14"],
          correctAnswer: 0,
        },
        {
          question: "What is the value of 2³ × 3?",
          options: ["24", "18", "15", "12"],
          correctAnswer: 0, // 2^3 = 8, 8*3=24. Original had 0, which is 12.
        },
        {
          question: "What is the value of 10 × (5 + 3)?",
          options: ["53", "80", "35", "18"],
          correctAnswer: 1,
        },
        {
          question: "What is the value of 14 × 14?",
          options: ["186", "196", "206", "156"],
          correctAnswer: 1,
        },
        {
          question: "What is the sum of the first 10 positive integers (1+2+...+10)?",
          options: ["50", "55", "60", "45"],
          correctAnswer: 1,
        },
        {
          question: "What is 12 × 15?",
          options: ["150", "160", "170", "180"],
          correctAnswer: 3,
        },
        {
          question: "What is the area of a circle with a radius of 3 cm? (Use π ≈ 3.14)",
          options: ["28.26 cm²", "18.84 cm²", "9.42 cm²", "31.40 cm²"],
          correctAnswer: 0, // A = pi * r^2 = 3.14 * 3^2 = 3.14 * 9 = 28.26
        },
        {
          question: "What is the value of (8 + 2) × 3?",
          options: ["30", "26", "13", "24"],
          correctAnswer: 0, // (8+2)=10, 10*3=30. Original had 3, which is 28.
        },
        {
          question: "What is 50% of 80?",
          options: ["30", "35", "40", "45"],
          correctAnswer: 2,
        },
        {
          question: "What is the value of 25 ÷ 5 × 3 (following order of operations)?",
          options: ["1.66", "15", "5", "75"],
          correctAnswer: 1, // 25/5 = 5, 5*3 = 15
        },
      ],
  },
  {
    category: "Entertainment",
    slug: "entertainment",
    icon: "Film",
    description: "Test your knowledge of movies, music, TV shows, and more.",
    questions: [
        {
          question: "Who won the Academy Award for Best Actor for their role in 'King Richard' (awarded in 2022)?",
          options: ["Benedict Cumberbatch", "Will Smith", "Andrew Garfield", "Denzel Washington"],
          correctAnswer: 1,
        },
        {
          question: "Which film won the Academy Award for Best Picture at the 93rd Academy Awards (for films released in 2020, awarded in 2021)?",
          options: ["The Father", "Minari", "Sound of Metal", "Nomadland"],
          correctAnswer: 3,
        },
        {
          question: "Who played the character of Jack Dawson in the 1997 movie 'Titanic'?",
          options: ["Leonardo DiCaprio", "Brad Pitt", "Johnny Depp", "Tom Cruise"],
          correctAnswer: 0,
        },
        {
          question: "Which popular TV show features the fictional continents of Westeros and Essos?",
          options: ["The Witcher", "Game of Thrones", "Vikings", "Lord of the Rings: The Rings of Power"],
          correctAnswer: 1,
        },
        {
          question: "Who is widely known by the nickname 'The King of Pop'?",
          options: ["Michael Jackson", "Prince", "Elvis Presley", "Stevie Wonder"],
          correctAnswer: 0,
        },
        {
          question: "Which Marvel superhero is known for the catchphrase, 'I am Iron Man'?",
          options: ["Captain America", "Thor", "Hulk", "Iron Man"],
          correctAnswer: 3,
        },
        {
          question: "Which iconic science fiction movie franchise includes characters like Luke Skywalker, Princess Leia, and Darth Vader?",
          options: ["Star Trek", "Star Wars", "Battlestar Galactica", "Dune"],
          correctAnswer: 1,
        },
        {
          question: "Who played the character of Hermione Granger in the Harry Potter film series?",
          options: ["Emma Watson", "Emma Stone", "Keira Knightley", "Natalie Portman"],
          correctAnswer: 0,
        },
        {
          question: "Who directed the mind-bending 2010 science fiction film 'Inception'?",
          options: ["James Cameron", "Steven Spielberg", "Christopher Nolan", "Denis Villeneuve"],
          correctAnswer: 2,
        },
        {
          question: "Which artist released the critically acclaimed album 'Folklore' in 2020?",
          options: ["Billie Eilish", "Taylor Swift", "Dua Lipa", "Ariana Grande"],
          correctAnswer: 1, // Lover was 2019, Folklore/Evermore were 2020.
        },
        {
          question: "What was the first arcade game released by Nintendo to feature the character Mario (originally named Jumpman)?",
          options: ["Mario Bros.", "Super Mario Bros.", "Donkey Kong", "Donkey Kong Jr."],
          correctAnswer: 2,
        },
        {
          question: "Which classic 1942 film features the famous line, 'Here's looking at you, kid.'?",
          options: ["Casablanca", "Citizen Kane", "The Maltese Falcon", "Gone with the Wind"],
          correctAnswer: 0,
        },
        {
          question: "Which country won the FIFA World Cup held in Russia in 2018?",
          options: ["France", "Croatia", "Brazil", "Germany"],
          correctAnswer: 0,
        },
        {
          question: "Who co-created the comic book character Spider-Man along with artist Steve Ditko?",
          options: ["Jack Kirby", "Stan Lee", "Joe Simon", "Bob Kane"],
          correctAnswer: 1,
        },
        {
          question: "In which Christopher Nolan film did Heath Ledger deliver an iconic performance as the Joker?",
          options: ["The Dark Knight", "Batman Begins", "The Dark Knight Rises", "Inception"],
          correctAnswer: 0,
        },
        {
          question: "Which legendary British rock band is known for the epic song 'Bohemian Rhapsody'?",
          options: ["The Rolling Stones", "Led Zeppelin", "Queen", "The Beatles"],
          correctAnswer: 2,
        },
        {
          question: "Which actress starred as Katniss Everdeen in 'The Hunger Games' film series?",
          options: ["Shailene Woodley", "Emma Stone", "Jennifer Lawrence", "Saoirse Ronan"],
          correctAnswer: 2,
        },
        {
          question: "Who won an Academy Award for Best Actor for playing Arthur Fleck in the 2019 film 'Joker'?",
          options: ["Adam Driver", "Leonardo DiCaprio", "Joaquin Phoenix", "Antonio Banderas"],
          correctAnswer: 2,
        },
        {
          question: "Which Disney animated film features the hit song 'A Whole New World'?",
          options: ["The Lion King", "Aladdin", "Beauty and the Beast", "The Little Mermaid"],
          correctAnswer: 1,
        },
        {
          question: "Which highly acclaimed TV series revolves around the characters Walter White, a chemistry teacher, and Jesse Pinkman, his former student?",
          options: ["Narcos", "Better Call Saul", "Ozark", "Breaking Bad"],
          correctAnswer: 3,
        },
        {
          question: "Who sang the global hit song 'Shape of You', released in 2017?",
          options: ["Justin Bieber", "Shawn Mendes", "Charlie Puth", "Ed Sheeran"],
          correctAnswer: 3,
        },
        {
          question: "Which film won the Academy Award for Best Picture at the 92nd Academy Awards (for films released in 2019, awarded in 2020)?",
          options: ["Joker", "Once Upon a Time in Hollywood", "Parasite", "1917"],
          correctAnswer: 2,
        },
        {
          question: "In what year was the influential science fiction film 'The Matrix' released?",
          options: ["1997", "2001", "2003", "1999"],
          correctAnswer: 3,
        },
        {
          question: "Which actor famously portrayed Tony Stark/Iron Man in the Marvel Cinematic Universe?",
          options: ["Chris Pratt", "Chris Evans", "Robert Downey Jr.", "Chris Hemsworth"],
          correctAnswer: 2,
        },
        {
          question: "Which iconic singer is often referred to as the 'Queen of Pop'?",
          options: ["Beyoncé", "Rihanna", "Britney Spears", "Madonna"],
          correctAnswer: 3,
        },
      ],
  },
];
