"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  MessageSquare,
  Compass,
  ChevronDown,
  Send,
  Moon,
  Sun,
  Mic,
  StopCircle,
  Download,
  Trash2,
} from "lucide-react";
// import botResponses from "./botResponses";

interface SuggestionProps {
  icon?: React.ReactNode;
  text: string;
  onClick: () => void;
}

interface Message {
  id: number;
  text: string;
  sender: "user" | "bot";
  timestamp: Date;
}

const Suggestion: React.FC<SuggestionProps> = ({ text, onClick }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
    className="flex items-center p-4 bg-white dark:bg-gray-700 rounded-lg shadow-md hover:bg-gray-50 dark:hover:bg-gray-600 cursor-pointer"
    onClick={onClick}
  >
    <span className="ml-2 text-sm">{text}</span>
  </motion.div>
);

const ChatbotPage: React.FC = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [conversationHistory, setConversationHistory] = useState<
    { title: string; messages: Message[] }[]
  >([]);
  const [currentConversation, setCurrentConversation] = useState<number | null>(
    null
  );

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognition = useRef<any>(null);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [darkMode]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if ("webkitSpeechRecognition" in window) {
      recognition.current = new (window as any).webkitSpeechRecognition();
      recognition.current.continuous = true;
      recognition.current.interimResults = true;

      recognition.current.onresult = (event: any) => {
        const transcript = Array.from(event.results)
          .map((result: any) => result[0])
          .map((result: any) => result.transcript)
          .join("");

        setInputValue(transcript);
      };

      recognition.current.onend = () => {
        setIsListening(false);
      };
    }
  }, []);

  const handleSendMessage = (text: string) => {
    if (text.trim() === "") return;

    const newMessage: Message = {
      id: Date.now(),
      text,
      sender: "user",
      timestamp: new Date(),
    };
    setMessages((prevMessages) => [...prevMessages, newMessage]);
    setInputValue("");
    setIsTyping(true);

    // Simulate bot response
    setTimeout(() => {
      const botMessage: Message = {
        id: Date.now(),
        text: generateBotResponse(text),
        sender: "bot",
        timestamp: new Date(),
      };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const generateBotResponse = (userInput: string): string => {
    const responses = {
      "how to apply online":
        "To apply online, visit our university's admissions website, create an account, fill out the application form, upload required documents, and submit the application fee. The process typically takes 30-45 minutes.",
      "how to register courses":
        "Course registration is done through our student portal. Log in, navigate to 'Course Registration', select your desired courses, and confirm your selection. Registration periods are announced via email.",
      "when is orientation week":
        "Orientation week is usually held the week before classes start. For the upcoming semester, it's scheduled for August 28th to September 1st. Check your student email for the detailed schedule.",
      "what are admission requirements":
        "Admission requirements vary by program but generally include: completed application form, official transcripts, standardized test scores (e.g., SAT/ACT for undergrads, GRE/GMAT for some graduate programs), letters of recommendation, and a personal statement.",
    };

    const lowercaseInput = userInput.toLowerCase();
    for (const [key, value] of Object.entries(responses)) {
      if (lowercaseInput.includes(key)) {
        return value;
      }
    }

    return "I'm sorry, I don't have specific information about that. Could you please rephrase your question or ask about something else?";
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  const toggleListening = () => {
    if (isListening) {
      recognition.current.stop();
    } else {
      recognition.current.start();
      setIsListening(true);
    }
  };

  const saveConversation = () => {
    if (messages.length > 0) {
      const title = messages[0].text.substring(0, 30) + "...";
      setConversationHistory((prev) => [...prev, { title, messages }]);
      setMessages([]);
      setCurrentConversation(null);
    }
  };

  const loadConversation = (index: number) => {
    setMessages(conversationHistory[index].messages);
    setCurrentConversation(index);
  };

  const deleteConversation = (index: number) => {
    setConversationHistory((prev) => prev.filter((_, i) => i !== index));
    if (currentConversation === index) {
      setMessages([]);
      setCurrentConversation(null);
    }
  };

  const exportConversation = () => {
    const conversationText = messages
      .map((m) => `${m.sender}: ${m.text}`)
      .join("\n");
    const blob = new Blob([conversationText], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "conversation.txt";
    a.click();
  };

  return (
    <div
      className={`flex h-screen ${
        darkMode
          ? "bg-gray-900 text-white"
          : "bg-gradient-to-br from-teal-50 to-blue-50"
      }`}
    >
      {/* Sidebar */}
      <motion.aside
        initial={{ x: -50, opacity: 0 }}
        animate={{ x: 0, opacity: 1 }}
        transition={{ duration: 0.5 }}
        className={`w-64 ${
          darkMode ? "bg-gray-800" : "bg-white"
        } p-4 flex flex-col shadow-lg`}
      >
        <div className="flex items-center justify-between mb-6">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2, duration: 0.4 }}
            className="flex items-center space-x-2"
          >
            <div
              className={`w-8 h-8 ${
                darkMode ? "bg-teal-600" : "bg-teal-200"
              } rounded-sm`}
            ></div>
            <span
              className={`font-semibold ${
                darkMode ? "text-teal-300" : "text-teal-700"
              }`}
            >
              Your Assistant
            </span>
          </motion.div>
          <ChevronDown
            className={`w-5 h-5 ${
              darkMode ? "text-teal-300" : "text-teal-500"
            }`}
          />
        </div>
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={saveConversation}
          className={`flex items-center justify-center space-x-2 ${
            darkMode
              ? "bg-teal-700 hover:bg-teal-600"
              : "bg-teal-100 hover:bg-teal-200"
          } rounded-md py-2 px-4 mb-4`}
        >
          <MessageSquare
            className={`w-4 h-4 ${
              darkMode ? "text-teal-200" : "text-teal-600"
            }`}
          />
          <span className={darkMode ? "text-teal-100" : "text-teal-700"}>
            New chat
          </span>
        </motion.button>
        <nav className="flex-1 overflow-y-auto">
          <h2
            className={`text-xs font-semibold ${
              darkMode ? "text-gray-400" : "text-gray-500"
            } mb-2`}
          >
            Conversations
          </h2>
          <ul className="space-y-2">
            {conversationHistory.map((conv, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 * index }}
                className={`flex justify-between items-center text-sm ${
                  darkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
                } rounded px-2 py-1 cursor-pointer`}
                onClick={() => loadConversation(index)}
              >
                <span>{conv.title}</span>
                <Trash2
                  className="w-4 h-4 text-gray-500 hover:text-red-500"
                  onClick={(e) => {
                    e.stopPropagation();
                    deleteConversation(index);
                  }}
                />
              </motion.li>
            ))}
          </ul>
        </nav>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.4 }}
          className="mt-auto"
        >
          <button
            className={`flex items-center space-x-2 ${
              darkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
            } rounded-md py-2 px-4 w-full mb-2`}
            onClick={() => setDarkMode(!darkMode)}
          >
            {darkMode ? (
              <Sun className="w-4 h-4 text-yellow-300" />
            ) : (
              <Moon className="w-4 h-4 text-teal-600" />
            )}
            <span
              className={`text-sm ${
                darkMode ? "text-gray-300" : "text-teal-700"
              }`}
            >
              {darkMode ? "Light Mode" : "Dark Mode"}
            </span>
          </button>
          <button
            className={`flex items-center space-x-2 ${
              darkMode ? "hover:bg-gray-700" : "hover:bg-gray-100"
            } rounded-md py-2 px-4 w-full`}
            onClick={exportConversation}
          >
            <Download
              className={`w-4 h-4 ${
                darkMode ? "text-teal-300" : "text-teal-600"
              }`}
            />
            <span
              className={`text-sm ${
                darkMode ? "text-gray-300" : "text-teal-700"
              }`}
            >
              Export Chat
            </span>
          </button>
        </motion.div>
      </motion.aside>

      {/* Main content */}
      <main
        className={`flex-1 p-8 flex flex-col ${darkMode ? "text-white" : ""}`}
      >
        <AnimatePresence>
          {messages.length === 0 && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 0.5 }}
              className="flex flex-col items-center flex-grow justify-center"
            >
              <div
                className={`w-16 h-16 ${
                  darkMode ? "bg-teal-600" : "bg-teal-200"
                } rounded-full mb-4`}
              ></div>
              <h1
                className={`text-3xl font-bold mb-8 ${
                  darkMode ? "text-teal-300" : "text-teal-700"
                }`}
              >
                Your Assistant
              </h1>
              <div className="grid grid-cols-2 gap-4 max-w-2xl w-full">
                <Suggestion
                  text="How to apply online?"
                  onClick={() => handleSuggestionClick("How to apply online?")}
                />
                <Suggestion
                  text="How to register courses?"
                  onClick={() =>
                    handleSuggestionClick("How to register courses?")
                  }
                />
                <Suggestion
                  text="When is orientation week?"
                  onClick={() =>
                    handleSuggestionClick("When is orientation week?")
                  }
                />
                <Suggestion
                  text="What are admission requirements?"
                  onClick={() =>
                    handleSuggestionClick("What are admission requirements?")
                  }
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {messages.length > 0 && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex-grow overflow-auto mb-4"
          >
            {messages.map((message) => (
              <motion.div
                key={message.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className={`mb-4 ${
                  message.sender === "user" ? "text-right" : "text-left"
                }`}
              >
                <div className={`inline-block max-w-md`}>
                  <span
                    className={`inline-block p-2 rounded-lg ${
                      message.sender === "user"
                        ? darkMode
                          ? "bg-teal-600"
                          : "bg-teal-200"
                        : darkMode
                        ? "bg-gray-700"
                        : "bg-white"
                    }`}
                  >
                    {message.text}
                  </span>
                  <div
                    className={`text-xs mt-1 ${
                      darkMode ? "text-gray-400" : "text-gray-500"
                    }`}
                  >
                    {message.timestamp.toLocaleTimeString()}
                  </div>
                </div>
              </motion.div>
            ))}
            {isTyping && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-left"
              >
                <span
                  className={`inline-block p-2 rounded-lg ${
                    darkMode ? "bg-gray-700" : "bg-white"
                  }`}
                >
                  GradGuru is typing...
                </span>
              </motion.div>
            )}
            <div ref={messagesEndRef} />
          </motion.div>
        )}

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="mt-auto w-full max-w-3xl mx-auto"
        >
          <div
            className={`flex items-center border ${
              darkMode ? "border-gray-600" : "border-gray-300"
            } rounded-lg overflow-hidden`}
          >
            <input
              type="text"
              placeholder="Type your message..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  handleSendMessage(inputValue);
                }
              }}
              className={`flex-1 px-4 py-2 ${
                darkMode ? "bg-gray-800 text-white" : "bg-white text-gray-900"
              } focus:outline-none`}
            />
            <button
              onClick={handleSendMessage.bind(null, inputValue)}
              className={`p-2 ${
                darkMode ? "bg-teal-700" : "bg-teal-200"
              } hover:${
                darkMode ? "bg-teal-600" : "bg-teal-300"
              } transition-colors`}
            >
              <Send
                className={`w-5 h-5 ${
                  darkMode ? "text-white" : "text-gray-800"
                }`}
              />
            </button>
            <button
              onClick={toggleListening}
              className={`p-2 ${
                isListening
                  ? darkMode
                    ? "bg-red-600"
                    : "bg-red-200"
                  : darkMode
                  ? "bg-gray-700"
                  : "bg-gray-200"
              } hover:${
                darkMode ? "bg-red-500" : "bg-gray-300"
              } transition-colors`}
            >
              {isListening ? (
                <StopCircle
                  className={`w-5 h-5 ${
                    darkMode ? "text-red-400" : "text-red-600"
                  }`}
                />
              ) : (
                <Mic
                  className={`w-5 h-5 ${
                    darkMode ? "text-gray-300" : "text-gray-600"
                  }`}
                />
              )}
            </button>
          </div>
        </motion.div>
      </main>
    </div>
  );
};

export default ChatbotPage;
