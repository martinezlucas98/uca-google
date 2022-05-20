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
  const res = await fetch('http://127.0.0.1:8000/search?q=' + query.q)
  console.log(res)

  let data = await res.json()
  
  console.log(query)
  data = JSON.parse(data);
  console.log(data)
  //console.log(typeof data)
  // Pass data to the page via props
  
  if(data.status == 'notfound'){
    data = {
      results:[
        {
          url: "No se encontro nada"
        }
      ]
    }
  }
  return { props: { data } }
}

export default results;