
import Results from './Results';
//import datos from './datos.json';
import styles from './Results.module.css';

function Show_results(props){
  return(
    <div>
    {
      props.datox.results.map(dato =>{
        return(
          <Results
          link={dato.url}
          description={dato.url}
        />
        )
      })
    }

    </div>

  );

}

export default Show_results;
