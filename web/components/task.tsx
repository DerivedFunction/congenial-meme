import React from "react";

interface TaskProps {
  title: string;
  description: string;
  onClick: () => void;
}

const Task: React.FC<TaskProps> = ({ title, description, onClick }) => {
  return (
    <button
      className="w-full text-left p-4 rounded-lg border border-gray-200 dark:border-gray-700/50 hover:border-gray-300 dark:hover:border-gray-600 bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300"
      onClick={onClick}
    >
      <div className="flex flex-col gap-1">
        <h3 className="font-medium text-gray-800 dark:text-gray-200">
          {title}
        </h3>
        <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
          {description}
        </p>
        <div className="flex items-center gap-2 mt-2 text-xs"></div>
      </div>
    </button>
  );
};

export default Task;
