/* eslint-disable @typescript-eslint/no-explicit-any */
interface ResultsTableProps {
  order: string;
  data: any[];
}

const ResultsTable: React.FC<ResultsTableProps> = ({ order, data }) => {
  if (!data || data.length === 0) return null;

  const lastResult = data[data.length - 1];
  if (!lastResult || lastResult.length === 0) {
    return <p>No results</p>;
  }

  // Get raw columns from the data
  const rawColumns = Object.keys(lastResult[0]);
  console.log(rawColumns)

  // Split order string and filter to only include columns that exist in rawColumns
  const orderColumns = order
    .split(" ")
    .filter((col) => col.trim() && rawColumns.includes(col));

  // Create a map for column order
  const orderMap = new Map<string, number>();
  orderColumns.forEach((col, index) => {
    orderMap.set(col, index);
  });


  // Sort columns: prioritize orderMap index, then alphabetical for unspecified columns
  const columns = rawColumns.sort((a, b) => {
    const aIndex = orderMap.has(a) ? orderMap.get(a)! : 999;
    const bIndex = orderMap.has(b) ? orderMap.get(b)! : 999;
    if (aIndex !== bIndex) {
      return aIndex - bIndex; // Sort by orderMap index
    }
    return a.localeCompare(b); // Alphabetical sort for unspecified columns
  });
  console.log("orderColumns:", orderColumns);
  console.log("orderMap:", Array.from(orderMap.entries()));
  console.log("sorted columns:", columns);

  return (
    <div className="mt-2 overflow-x-auto">
      <table className="w-full border-collapse border border-gray-300 dark:border-gray-600">
        <thead>
          <tr className="bg-gray-100 dark:bg-gray-700">
            <th className="border border-gray-300 dark:border-gray-600 p-2 text-left">
              #
            </th>
            {columns.map((col) => (
              <th
                key={col}
                className="border border-gray-300 dark:border-gray-600 p-2 text-left"
              >
                {col.toUpperCase()}
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
                  {row[col] !== null && row[col] !== undefined
                    ? row[col]
                    : "NULL"}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ResultsTable;
