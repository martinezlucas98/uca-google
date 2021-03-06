import Head from 'next/head'
import SearchBar from '../components/SearchBar/SearchBar'
import styles from '../styles/Home.module.css'
import UcaLogo from '../components/UcaLogo/UcaLogo'

export default function Home() {
  return (
    <div className={styles.container}>
      <div className={styles.main}>
        <Head>
          <title>Uca Google</title>
          <meta name="description" content="Generated by create next app" />
          <link rel="icon" href="/favicon.ico" />
        </Head>
        
      
          <UcaLogo />
          <SearchBar/>
      
      </div>
      <footer className={styles.footer}>
        <a
          href="https://github.com/martinezlucas98/uca-google/"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by{' '}
          <span className={styles.logo}>
            UCA-Google
          </span>
        </a>
      </footer>
    </div>
  )
}
