import React from 'react';
import Head from 'next/head';
import Header from './Header';

const Layout = ({ children, title = "My Tasks" }) => {
  return (
    <>
      <Head>
        <title>{title}</title>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-white dark:bg-navy-blue text-navy-blue dark:text-white">
        <Header />
        <main className="container mx-auto px-4 py-8 max-w-4xl">
          {children}
        </main>
      </div>
    </>
  );
};

export default Layout;
