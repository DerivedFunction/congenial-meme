import { useState } from "react";
import think from "../src/images/think.svg";
import file from "../src/images/file.svg";
import send from "../src/images/send.svg";
const PromptBox = () => {
  const [prompt, setPrompt] = useState("");
  const [reason, setReason] = useState(false);
  return (
    <form
      className={`w-full bg-white dark:bg-gray-800 p-4 rounded-3xl mt-4 transition-all shadow-sm max-w-3xl`}
    >
      <textarea
        className="outline-none w-full resize-none overflow-hidden break-words bg-transparent text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500 rounded-md p-2"
        rows={2}
        placeholder="Enter your prompt here..."
        onChange={(e) => setPrompt(e.target.value)}
        value={prompt}
        required
      />

      <div className="flex items-center justify-between text-sm">
        <div
          className="flex items-center gap-2"
          onClick={() => setReason(!reason)}
        >
          <p
            className={`flex items-center gap-2 text-xs border px-2 py-1 rounded-full cursor-pointer transition-colors ${
              reason
                ? "bg-blue-100 border-blue-400 text-blue-800 dark:bg-blue-900 dark:border-blue-600 dark:text-blue-200"
                : "border-gray-300 text-gray-600 dark:border-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            <img
              className={`h-5 ${
                reason ? "opacity-100" : "opacity-70"
              } dark:invert`}
              src={think}
              alt="Reason"
              width={20}
              height={20}
            />
            Reason
          </p>
        </div>

        <div className="flex items-center gap-2">
          <img
            className="w-4 cursor-pointer dark:invert"
            src={file}
            width={20}
            height={20}
            alt="pin icon"
          />
          <button
            className={`rounded-full p-2 transition-colors ${
              prompt.length > 0
                ? "bg-blue-600 hover:bg-blue-700 text-white dark:bg-blue-500 dark:hover:bg-blue-600"
                : "bg-gray-300 text-gray-500 cursor-not-allowed dark:bg-gray-600 dark:text-gray-400"
            }`}
            disabled={prompt.length === 0}
          >
            <img
              className="w-3.5 aspect-square dark:invert"
              src={send}
              alt=""
              height={20}
              width={20}
            />
          </button>
        </div>
      </div>
    </form>
  );
};

export default PromptBox;
