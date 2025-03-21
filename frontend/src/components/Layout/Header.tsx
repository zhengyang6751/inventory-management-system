import React from "react";
import { Link } from "react-router-dom";
import { Menu } from "@headlessui/react";
import { UserCircleIcon, BellIcon } from "@heroicons/react/24/outline";
import { useAuth } from "@/hooks/useAuth";

export default function Header() {
  const { user, logout } = useAuth();

  return (
    <header className="bg-white shadow-sm">
      <div className="mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 justify-between">
          <div className="flex">
            <div className="flex flex-shrink-0 items-center">
              <h1 className="text-xl font-bold text-gray-900">
                Inventory Management
              </h1>
            </div>
          </div>

          <div className="flex items-center">
            <button
              type="button"
              className="rounded-full bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none"
            >
              <BellIcon className="h-6 w-6" />
            </button>

            <Menu as="div" className="relative ml-3">
              <Menu.Button className="flex rounded-full bg-white text-sm focus:outline-none">
                <UserCircleIcon className="h-8 w-8 text-gray-400" />
              </Menu.Button>

              <Menu.Items className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md bg-white py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <Menu.Item>
                  {({ active }) => (
                    <Link
                      to="/profile"
                      className={`${
                        active ? "bg-gray-100" : ""
                      } block px-4 py-2 text-sm text-gray-700`}
                    >
                      Your Profile
                    </Link>
                  )}
                </Menu.Item>
                <Menu.Item>
                  {({ active }) => (
                    <button
                      onClick={logout}
                      className={`${
                        active ? "bg-gray-100" : ""
                      } block w-full px-4 py-2 text-left text-sm text-gray-700`}
                    >
                      Sign out
                    </button>
                  )}
                </Menu.Item>
              </Menu.Items>
            </Menu>
          </div>
        </div>
      </div>
    </header>
  );
}
