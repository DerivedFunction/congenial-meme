import { useState, type JSX } from "react";
import Sidebar from "./../components/sidebar";
import DatabasePage from "./../pages/database";
import "./App.css";

function App() {
  const [expand, setExpand] = useState(false);
  const [isHovered, setIsHovered] = useState(false);
  type ComponentKey = "newTask" | "manageDB";
  const [activeComponent, setActiveComponent] =
    useState<ComponentKey>("newTask");

  // Component mapping (better than switch statement)
  const components: Record<ComponentKey, JSX.Element> = {
    newTask: <></>,
    manageDB: <DatabasePage />,
    // Add other components here
  };
  return (
    <>
      <div className="relative flex h-screen overflow-hidden">
        <div className="md:hidden fixed top-1 left-1 z-[60]">
          {!expand && (
            <button
              onClick={() => setExpand(true)}
              className="flex items-center justify-center h-9 w-9 rounded-lg hover:bg-gray-500/20 transition-all duration-300"
            >
              <img
                src="./menu.svg"
                width={20}
                height={20}
                className="dark:invert"
              />
            </button>
          )}
        </div>
        <Sidebar
          expand={expand}
          setExpand={setExpand}
          isHovered={isHovered}
          setIsHovered={setIsHovered}
          setActiveComponent={setActiveComponent}
        />
        <main
          className={`flex-1 transition-all duration-300 overflow-y-auto flex flex-col justify-between ${
            expand ? "md:ml-64" : "md:ml-12"
          }`}
        >
          {components[activeComponent]}
        </main>
      </div>
    </>
  );
}

export default App;
