import SearchBar from '../components/SearchBar/SearchBar';
import Show_results from '../components/Results/Show-results';
import styles from '../styles/results.module.css'


function results() {

  return(
    <div className={styles.wrapper}>
      <div className={styles.search_bar}>
        <SearchBar/>
        
      </div>

      <div className={styles.results}>
        <Show_results />
       
      </div>

     
    </div>
    
    
  );
}

export default results;