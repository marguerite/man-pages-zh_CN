;; doclifter.el -- lift markup in a manual page converted by doclifter

(defun lift-next ()
  "Lift the next remapped emphasis highlight."
  (interactive)
  (if (re-search-forward "<emphasis remap='[A-Z]*'>[^<]*</emphasis>" nil t)
      (progn
	(let ((start (match-beginning 0)) (end (match-end 0)))
	  (add-text-properties start end '(background-color . "green"))
	  (call-interactively 'lift-at-point)
	  (remove-text-properties start end nil)
	  t))
    )
  )

(defun lift-at-point (type)
  "Lift a remapped emphasis highlight starting at point."
  (interactive "sTag: ")
  (if (re-search-forward "<emphasis remap='[A-Z]*'>\\([^<]*\\)</emphasis>")
      (replace-match (concat "<" type ">\\1</" type ">") t nil)))

(defun bump-sendcounts ()
  "Bump send counts on each piece of bugmail."
  (interactive)
  (if (re-search-forward "%%" nil t)
      (progn
	(forward-line 1)
	(while (not (eobp))
	  (cond ((looking-at "[yb]")
		 nil)
		((looking-at "[0-9]+")
		 (let* ((s (match-beginning 0))
			(e (match-end 0))
			(d (buffer-substring s e)))
		   (delete-region s e)
		   (insert-string (format "%d" (1+ (string-to-number d))))
		   ))
		(t
		 (insert-string "1")))
	  (forward-line 1))
	)))
    
;; End
