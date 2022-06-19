preds = model_predict(file_path, Model)
pred_class = preds.argmax(axis=-1)
pr = lesion_classes_dict[pred_class[0]]
result = str(pr)

return render_template('home.html', result=result, filename=filename)

 <ul class="actions">
											<li><a href="{{ url_for('upload') }}" class="button">Upload Image</a></li>
										</ul>