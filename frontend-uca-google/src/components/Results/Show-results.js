
import Results from './Results';
import datos from './datos.json';
import styles from './Results.module.css';

function Show_results(){
  return(
    <div>
    {
      datos.map(dato =>{
        return(
          <Results
          link={dato.link}
          description={dato.description}
        />
        )
      })
    }

    </div>

  );

}

export default Show_results;
