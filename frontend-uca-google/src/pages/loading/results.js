import SearchBar from '../../components/SearchBar/SearchBar';
import Results from '../../components/Loading/Results';
import styles from '../../styles/results.module.css'
import UcaLogo from '../../components/UcaLogo/UcaLogo';
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';


function results({data}) {
  const router = useRouter()
  useEffect(() => {
      router.replace(`/results/${router.query.q}`);
  })
  return(
    
    <div className={styles.wrapper}>
      {/* <div className={styles.logo}>
        <UcaLogo/>
      </div> */}
     
      <div className={styles.search_bar}>
        <SearchBar/>
        
      </div>

      <div className={styles.container_loading}>
       
          <Results/>
          <Results/>
          <Results/>
          
        
       
      </div>
    

     
    </div>
    
    
  );
}




export default results;