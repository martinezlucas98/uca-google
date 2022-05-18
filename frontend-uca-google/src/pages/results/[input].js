import SearchBar from '../../components/SearchBar/SearchBar';
import Show_results from '../../components/Results/Show-results';
import styles from '../../styles/results.module.css'


function results({data}) {

  return(
    <div className={styles.wrapper}>
      <div className={styles.search_bar}>
        <SearchBar/>
        
      </div>

      <div className={styles.results}>
        <Show_results datox={data}/>
       
      </div>

     
    </div>
    
    
  );
}

// This gets called on every request
export async function getServerSideProps({query}) {
  // Fetch data from external API
  console.log(query.q)
  const res = await fetch('https://jsonplaceholder.typicode.com/users')
  const data = await res.json()
  console.log(data)
  // Pass data to the page via props
  return { props: { data } }
}

export default results;