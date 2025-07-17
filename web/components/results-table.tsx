/* eslint-disable @typescript-eslint/no-explicit-any */
import React from "react";

interface ResultsTableProps {
  data: any[];
}

const ResultsTable: React.FC<ResultsTableProps> = ({ data }) => {
  if (!data || data.length === 0) return null;

  const lastResult = data[data.length - 1];
  if (!lastResult || lastResult.length === 0) {
    return <p>No results</p>;
  }

  const columns = Object.keys(lastResult[0]);

  return (
    <div className="mt-2">
      <table className="w-full border-collapse border border-gray-300 dark:border-gray-600">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-700">
            <th className="border border-gray-300 dark:border-gray-600 p-2">
              #
            </th>
            {columns.map((col) => (
              <th
                key={col}
                className="border border-gray-300 dark:border-gray-600 p-2"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {lastResult.map((row: any, index: number) => (
            <tr key={index} className="hover:bg-gray-50 dark:hover:bg-gray-700">
              <td className="border border-gray-300 dark:border-gray-600 p-2">
                {index + 1}
              </td>
              {columns.map((col) => (
                <td
                  key={col}
                  className="border border-gray-300 dark:border-gray-600 p-2"
                >
                  {row[col] !== null ? row[col] : "NULL"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="mt-2 flex space-x-2">
        <button className="p-2 bg-green-500 text-white rounded-md">
          Download CSV
        </button>
        <button className="p-2 bg-green-500 text-white rounded-md">
          Download JSON
        </button>
        <button className="p-2 bg-purple-500 text-white rounded-md">
          Download MD Table
        </button>
      </div>
    </div>
  );
};

export default ResultsTable;
