<script src="//code.jquery.com/jquery-1.11.1.min.js"></script>

<!DOCTYPE html>
<html lang="fr" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title>Greenfeed 91</title>
    <link href="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet" id="bootstrap-css">
    <script src="//netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>
    <link rel="stylesheet" href="css/bootstrap.min.css">
		<link rel="stylesheet" href="css/style.css">

  </head>
  <body>
    <div class="container-fluide">

    <!-------->
    <div id="content">
        <ul id="tabs" class="nav nav-tabs onglet" data-tabs="tabs">
            <li><a href="#red" data-toggle="tab">Greenfeed 90</a></li>
            <li class="active"><a href="#orange" data-toggle="tab">Greenfeed 91</a></li>
        </ul>
        <div id="my-tab-content" class="tab-content">
            <div class="tab-pane" id="red">
                <h1>Red</h1>
                <p>red red red red red red</p>
            </div>
            <div class="tab-pane active" id="orange">
              <div class="container-fluid entête">
                <div class="row">
                  <div class="col-md-1 bouton">
                    <?php
                    $len_col=count(file('colData'));
                    if (substr(cellule('colData',$len_col,1),0,6)=='Online')
                      echo'<img src="image/bouton_online.png" alt="logo online" width=75px />';
                    elseif (cellule('colData',$len_col,1)=='Offline')
                      echo'<img src="image/bouton_offline.png" alt="logo online" width=75px />';
                    else
                      echo'<img src="image/bouton_autre.png" alt="logo online" width=75px />';
                    ?>
                  </div>
                  <div class="col-md-4 statut">
                    <?php
                    $len_col=count(file('colData'));
                    echo cellule('colData',$len_col,0).' :  '.cellule('colData',$len_col,1);
                    ?>
                  </div>
                  <div class="col-md-6 colonne-centree">
                    <img src="image/Logo_CRA-W.png" alt="logo CRA-W" />
                  </div>
                  <div class="col-md-1 statut">
                    <?php
                    $len_col=count(file('colData'));
                    echo cellule('colData',$len_col-1,1);
                    ?>
                  </div>
                </div>

              </div>
              <div class="container">
                <div class="row contenu">
                  <div class="col-md-4 col">
                    <div class="row">
                      <div class="col-md-6 nomcol">
                        <?php
                        $len_col=count(file('colData'));
                        for ($k=1;$k<=$len_col-2;$k++){
                          echo cellule('colData',$k,0)." :   <br/><br/>";
                        }
                         ?>
                      </div>
                      <div class="col-md-6 valcol">
                        <?php
                        $len_col=count(file('colData'));
                        for ($k=1;$k<=$len_col-2;$k++){
                          echo cellule('colData',$k,1)."<br/><br/>";
                        }
                         ?>
                      </div>

                    </div>

                  </div>
                  <div class="col-md-4 tableau">
                    <?php
                    echo '<table>';
                    for ($k=1;$k<=$len_col-1;$k++){
                      echo "<tr>";
                      for($i=0;$i<=10;$i++){
                        echo '<td>'.cellule('Tableau',$k,$i).'<td>';
                      } echo '</tr>';
                    }
                    echo '</table>';
                     ?>
                  </div>
                </div>

              </div>
              <?php
              //lecture d'un fichier cellule par cellule
              //ligne 1-10
              //colonne 0-9
              function cellule($csv, $lig, $col){
              	$fic=fopen($csv,'r');
              	$len=count(file($csv));
              	for ($i=1;$i<=$lig;$i++){
              		$ligne=fgetcsv($fic,1024,',');
              	}
              	fclose($fic) ;
              	return $ligne[$col];
              }
              ?>
            </div>
        </div>
    </div>
  </body>
</html>
