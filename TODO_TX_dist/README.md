# TX distance analysis

Previous analysis showed problems when the distance of the receivers (RX) from the cylinders is increased: the RMSE increases significantly. In this setup, the transmitters (TX) are placed at the Fraunhofer distance.

Placing the TX farther away (10e6 m) improves the results, but in the deep shadow region the ray tracer is unable to compute the field.

At intermediate distances, the ray tracer does not always manage to compute the field, and this behavior is not yet predictable.

TODO: Investigate the causes of these issues (RMSE increase at large RX distances, missing field computation in the deep shadow region and at intermediate TX distances). 
