import Task from "../components/task";
const TaskPage = () => {
  return (
    <div className="flex items-start justify-center p-4 flex-1">
      <div className="w-full max-w-3xl space-y-3 py-12">
        <h2 className="text-center text-lg font-medium text-gray-700 dark:text-gray-300 mb-6">
          Select a task to start
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <Task
            title={"Import Roster Data"}
            description={"Import data from CSV"}
            onClick={() => {
              // Open the import roster modal
            }}
          />
        </div>
      </div>
    </div>
  );
};
export default TaskPage;
