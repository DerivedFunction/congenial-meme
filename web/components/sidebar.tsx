import React, { type Dispatch, type SetStateAction } from "react";
import NavItem from "./nav-item";
import menu_close from "../src/images/menu_close.svg";
import menu_open from "../src/images/menu_open.svg";
import menu from "../src/images/menu.svg";
import new_chat from "../src/images/new_chat.svg";
import database from "../src/images/database.svg";
interface SidebarProps {
  expand: boolean;
  setExpand: (expand: boolean) => void;
  isHovered: boolean;
  setIsHovered: (isHovered: boolean) => void;
  setActiveComponent: Dispatch<SetStateAction<"newTask" | "manageDB">>;
}

const Sidebar: React.FC<SidebarProps> = ({
  expand,
  setExpand,
  isHovered,
  setIsHovered,
  setActiveComponent,
}) => {
  return (
    <>
      <div
        className={`fixed top-0 left-0 h-screen transition-all z-50 bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 ${
          expand
            ? "w-64 shadow-lg md:shadow-none"
            : "md:w-12 w-0 max-md:opacity-0"
        }`}
      >
        <div className="flex flex-col h-full p-1">
          <div className="md:block hidden">
            <div
              onMouseEnter={() => setIsHovered(true)}
              onMouseLeave={() => setIsHovered(false)}
              className="group relative flex items-center justify-center hover:bg-gray-500/20 transition-all duration-300 h-9 w-9 aspect-square rounded-lg cursor-pointer"
            >
              <img
                src={expand ? menu_close : isHovered ? menu_open : menu}
                width={20}
                height={20}
                alt="Toggle menu"
                onClick={() => setExpand(!expand)}
                className="dark:invert"
              />
            </div>
          </div>
          <div className="md:hidden flex justify-end pr-2">
            <div className="group relative flex items-center justify-center hover:bg-gray-500/20 transition-all duration-300 h-9 w-9 aspect-square rounded-lg cursor-pointer">
              <img
                src={menu_close}
                width={20}
                height={20}
                alt="Close menu"
                onClick={() => setExpand(false)}
                className="dark:invert"
              />
            </div>
          </div>
          <div className="pt-10">
            <NavItem
              image={new_chat}
              text={"New Task"}
              expand={expand}
              onClick={() => setActiveComponent("newTask")}
            />
            <NavItem
              image={database}
              text={"Manage SQLite DB"}
              expand={expand}
              onClick={() => setActiveComponent("manageDB")}
            />
          </div>
        </div>
      </div>
      {/* Overlay for mobile */}
      {expand && (
        <div
          className="fixed inset-0 bg-black/40 z-40 md:hidden"
          onClick={() => setExpand(false)}
        />
      )}
    </>
  );
};

export default Sidebar;
