import React, { useRef } from "react";

export default function ImageUpload({ file, previewUrl, onFileChange, disabled }) {
  const inputRef = useRef(null);

  const handleChange = (e) => {
    const picked = e.target.files?.[0];
    if (picked) onFileChange(picked);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    const dropped = e.dataTransfer.files?.[0];
    if (dropped && dropped.type.startsWith("image/")) {
      onFileChange(dropped);
    }
  };

  return (
    <div className="upload-card">
      <h2>Загрузите фото</h2>
      <div
        className="dropzone"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={handleDrop}
        role="button"
        tabIndex={0}
        aria-label="Загрузить изображение еды"
      >
        {previewUrl ? (
          <img src={previewUrl} alt="Превью еды" className="preview" />
        ) : (
          <div className="dropzone-placeholder">
            <span className="dropzone-icon">🍽️</span>
            <p>Перетащите фото сюда или нажмите, чтобы выбрать</p>
            <small>JPG, JPEG, PNG — до 10 МБ</small>
          </div>
        )}
      </div>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        onChange={handleChange}
        disabled={disabled}
        data-testid="file-input"
        hidden
      />
      {file && <p className="filename">{file.name}</p>}
    </div>
  );
}
